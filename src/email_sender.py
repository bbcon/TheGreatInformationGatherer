"""
Email sending module for delivering video summaries.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from datetime import datetime


class EmailSender:
    """Handles sending summary emails via SMTP."""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        from_address: str
    ):
        """
        Initialize email sender.

        Args:
            smtp_server: SMTP server hostname (e.g., smtp.gmail.com)
            smtp_port: SMTP server port (typically 587 for TLS)
            username: SMTP username
            password: SMTP password or app password
            from_address: Email address to send from
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_address = from_address

    def send_summary(
        self,
        to_address: str,
        subject: str,
        html_body: str,
        plain_text_body: Optional[str] = None
    ) -> bool:
        """
        Send a summary email.

        Args:
            to_address: Recipient email address
            subject: Email subject line
            html_body: HTML formatted email body
            plain_text_body: Optional plain text version (fallback)

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_address
            msg['To'] = to_address
            msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

            # Add plain text version if provided
            if plain_text_body:
                part1 = MIMEText(plain_text_body, 'plain')
                msg.attach(part1)

            # Add HTML version
            part2 = MIMEText(html_body, 'html')
            msg.attach(part2)

            # Connect and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Upgrade to secure connection
                server.login(self.username, self.password)
                server.send_message(msg)

            print(f"Email sent successfully to {to_address}")
            return True

        except smtplib.SMTPAuthenticationError:
            print("SMTP authentication failed. Check your username and password.")
            print("For Gmail, you may need to use an App Password instead of your regular password.")
            return False
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {e}")
            return False
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_summary_with_video_data(
        self,
        to_address: str,
        summary_html: str,
        video_title: str,
        plain_text_summary: Optional[str] = None
    ) -> bool:
        """
        Send a summary email with automatic subject line generation.

        Args:
            to_address: Recipient email address
            summary_html: HTML formatted summary
            video_title: Video title for subject line
            plain_text_summary: Optional plain text version

        Returns:
            True if email sent successfully, False otherwise
        """
        # Generate subject line
        date_str = datetime.now().strftime('%Y-%m-%d')
        subject = f"📊 Macro Trading Summary - {date_str}: {video_title}"

        return self.send_summary(
            to_address=to_address,
            subject=subject,
            html_body=summary_html,
            plain_text_body=plain_text_summary
        )

    def test_connection(self) -> bool:
        """
        Test SMTP connection and authentication.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
            print("SMTP connection test successful!")
            return True
        except Exception as e:
            print(f"SMTP connection test failed: {e}")
            return False
