#!/usr/bin/env python3
"""
Newsletter Summarizer - Automated Daily Email Summary
Checks inbox for specific newsletter → Summarizes → Sends you summary
"""

import os
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import re
from pathlib import Path

from dotenv import load_dotenv
from anthropic import Anthropic
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment
load_dotenv()


class NewsletterSummarizer:
    """Automated newsletter summarization from email"""
    
    def __init__(self):
        # Email settings
        self.imap_server = os.getenv('IMAP_SERVER', 'imap.gmail.com')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')  # App password for Gmail
        
        # Newsletter settings
        self.newsletter_from = os.getenv('NEWSLETTER_FROM')  # Sender email
        self.newsletter_subject = os.getenv('NEWSLETTER_SUBJECT_CONTAINS', '')
        
        # AI settings
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        # Output settings
        self.send_to = os.getenv('SUMMARY_SEND_TO', self.email_address)
    
    def connect_to_inbox(self):
        """Connect to email inbox via IMAP"""
        print(f"Connecting to {self.imap_server}...")
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.email_address, self.email_password)
        mail.select('inbox')
        return mail
    
    def find_todays_newsletter(self, mail):
        """Find today's newsletter email"""
        print(f"Looking for newsletter from: {self.newsletter_from}")
        
        # Search for emails from today
        today = datetime.now().strftime('%d-%b-%Y')
        
        # Build search criteria
        search_criteria = f'(FROM "{self.newsletter_from}" SINCE {today})'
        
        if self.newsletter_subject:
            search_criteria = f'(FROM "{self.newsletter_from}" SUBJECT "{self.newsletter_subject}" SINCE {today})'
        
        status, messages = mail.search(None, search_criteria)
        
        if status != 'OK':
            print("No messages found!")
            return None
        
        email_ids = messages[0].split()
        
        if not email_ids:
            print("No newsletter received today yet.")
            return None
        
        # Get the most recent email
        latest_email_id = email_ids[-1]
        
        status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
        
        if status != 'OK':
            return None
        
        # Parse email
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        
        return email_message
    
    def extract_email_content(self, email_message):
        """Extract text content from email"""
        subject = self.decode_subject(email_message['Subject'])
        from_addr = email_message['From']
        date = email_message['Date']
        
        print(f"\nFound email:")
        print(f"  From: {from_addr}")
        print(f"  Subject: {subject}")
        print(f"  Date: {date}")
        
        # Extract body
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        pass
                elif content_type == "text/html" and not body:
                    try:
                        html_body = part.get_payload(decode=True).decode()
                        body = self.html_to_text(html_body)
                    except:
                        pass
        else:
            try:
                body = email_message.get_payload(decode=True).decode()
            except:
                body = str(email_message.get_payload())
        
        return {
            'subject': subject,
            'from': from_addr,
            'date': date,
            'body': body
        }
    
    def decode_subject(self, subject):
        """Decode email subject"""
        if subject is None:
            return ""
        
        decoded_parts = decode_header(subject)
        decoded_subject = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_subject += part.decode(encoding or 'utf-8')
                except:
                    decoded_subject += part.decode('utf-8', errors='ignore')
            else:
                decoded_subject += part
        
        return decoded_subject
    
    def html_to_text(self, html):
        """Convert HTML to plain text (basic)"""
        # Remove HTML tags
        text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def summarize_content(self, email_data):
        """Generate AI summary of newsletter"""
        print("\nGenerating AI summary...")
        
        prompt = f"""Please provide a concise, actionable summary of this newsletter.

Newsletter: {email_data['subject']}
Date: {email_data['date']}

Content:
{email_data['body'][:15000]}  

Please structure your summary as:

## Key Takeaways
[3-5 bullet points of the most important insights]

## Main Topics
[Brief overview of main sections/topics covered]

## Action Items
[Any actionable recommendations or items to follow up on]

Keep it concise and focused on what's most valuable."""

        try:
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            summary = response.content[0].text
            
            return summary
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None
    
    def send_summary_email(self, original_email, summary):
        """Send summary via email"""
        print(f"\nSending summary to {self.send_to}...")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_address
        msg['To'] = self.send_to
        msg['Subject'] = f"📋 Summary: {original_email['subject']}"
        
        # Create email body
        email_body = f"""
Newsletter Summary
{'='*60}

Original Newsletter: {original_email['subject']}
From: {original_email['from']}
Date: {original_email['date']}

{'='*60}

{summary}

{'='*60}

This summary was automatically generated.
Original newsletter is in your inbox.
"""
        
        msg.attach(MIMEText(email_body, 'plain'))
        
        try:
            # Connect and send
            with smtplib.SMTP_SSL(self.smtp_server, 465) as server:
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            print("✅ Summary sent successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def save_summary(self, original_email, summary):
        """Save summary to file"""
        output_dir = Path('output/summaries')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        today = datetime.now().strftime('%Y-%m-%d')
        filename = output_dir / f"{today}_newsletter_summary.txt"
        
        content = f"""Newsletter Summary - {today}
{'='*60}

Original: {original_email['subject']}
From: {original_email['from']}
Date: {original_email['date']}

{'='*60}

{summary}

{'='*60}
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Summary saved to: {filename}")
        
        # Create latest symlink
        latest = output_dir.parent / 'latest_summary.txt'
        with open(latest, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
    
    def run(self):
        """Main execution"""
        print("="*60)
        print("Newsletter Summarizer - Starting")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        try:
            # Connect to inbox
            mail = self.connect_to_inbox()
            
            # Find newsletter
            email_message = self.find_todays_newsletter(mail)
            
            if not email_message:
                print("No newsletter found today. Exiting.")
                return 1
            
            # Extract content
            email_data = self.extract_email_content(email_message)
            
            # Generate summary
            summary = self.summarize_content(email_data)
            
            if not summary:
                print("Failed to generate summary.")
                return 1
            
            # Save summary
            self.save_summary(email_data, summary)
            
            # Send summary email
            self.send_summary_email(email_data, summary)
            
            # Close connection
            mail.close()
            mail.logout()
            
            print("\n" + "="*60)
            print("Newsletter Summarizer - Completed Successfully!")
            print("="*60)
            
            return 0
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1


def main():
    summarizer = NewsletterSummarizer()
    return summarizer.run()


if __name__ == "__main__":
    exit(main())
