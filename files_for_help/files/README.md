# 📧 Newsletter Summarizer

Automatically summarizes your daily email newsletters using AI and sends you concise summaries.

## 💰 Cost: ~$0.10-0.20 per newsletter

- Uses Claude to generate smart summaries
- Only pay for what you use (pay-as-you-go)
- ~$3-6/month for daily newsletter

## How It Works

```
1. Script checks your inbox (IMAP)
2. Finds today's newsletter from specific sender
3. Extracts and cleans the content
4. Uses Claude AI to generate smart summary
5. Emails you the summary (or saves to file)
```

## Features

✅ **Automatic Detection** - Finds newsletter by sender/subject  
✅ **Smart Summarization** - Key takeaways, main topics, action items  
✅ **Email Delivery** - Get summary in your inbox  
✅ **File Archive** - Saves summaries for later reference  
✅ **Scheduled Runs** - Set it and forget it (cron)  
✅ **Multi-Newsletter** - Can handle multiple newsletters  

---

## Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
pip install anthropic python-dotenv
```

### 2. Gmail App Password Setup

**Why needed:** Gmail requires "App Passwords" for script access (more secure than your regular password)

**Steps:**
1. Go to https://myaccount.google.com/security
2. Enable **2-Factor Authentication** (required for app passwords)
3. Go to https://myaccount.google.com/apppasswords
4. Select **Mail** and **Other (Custom name)**
5. Name it: "Newsletter Summarizer"
6. Copy the 16-character password (looks like: `xxxx xxxx xxxx xxxx`)

### 3. Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit with your settings
nano .env
```

**Required settings:**
```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx  # App password from step 2
NEWSLETTER_FROM=newsletter@sender.com  # Who sends your newsletter
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

### 4. Test It

```bash
python3 main.py
```

If your newsletter arrived today, you'll get a summary!

---

## Configuration Examples

### Example 1: Morning Brew
```env
EMAIL_ADDRESS=you@gmail.com
EMAIL_PASSWORD=your-app-password
NEWSLETTER_FROM=crew@morningbrew.com
NEWSLETTER_SUBJECT_CONTAINS=Morning Brew
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

### Example 2: Stratechery
```env
NEWSLETTER_FROM=ben@stratechery.com
NEWSLETTER_SUBJECT_CONTAINS=
```

### Example 3: TechCrunch Daily
```env
NEWSLETTER_FROM=newsletter@techcrunch.com
NEWSLETTER_SUBJECT_CONTAINS=Daily Crunch
```

---

## Automation Setup

### Run Daily at 8 AM

```bash
# Edit crontab
crontab -e

# Add this line (adjust path):
0 8 * * * cd /path/to/newsletter-summarizer && python3 main.py >> logs/cron.log 2>&1
```

### Run After Newsletter Usually Arrives

If your newsletter arrives at 6 AM daily:
```bash
# Run at 6:30 AM
30 6 * * * cd /path/to/newsletter-summarizer && python3 main.py
```

### Multiple Newsletters

Create separate .env files:

```bash
# Morning newsletter at 7 AM
0 7 * * * cd /path/to/newsletter-summarizer && env $(cat .env.morning) python3 main.py

# Evening newsletter at 6 PM
0 18 * * * cd /path/to/newsletter-summarizer && env $(cat .env.evening) python3 main.py
```

---

## Advanced Features

### Custom Summary Style

Edit `main.py` and customize the prompt:

```python
prompt = f"""Summarize this newsletter focusing on:
1. Investment opportunities mentioned
2. Risk factors highlighted
3. Specific stock tickers discussed

Keep it under 200 words..."""
```

### Forward Instead of New Email

Want to forward with summary instead of new email?

```python
# In send_summary_email method:
msg['Subject'] = f"Fwd: {original_email['subject']}"
# Include original email body below summary
```

### Save to Notion/Obsidian

Add to `save_summary` method:

```python
# Copy to Notion inbox
import shutil
notion_inbox = Path.home() / 'Notion' / 'Inbox'
shutil.copy(filename, notion_inbox)
```

### Slack Integration

```python
from slack_sdk import WebClient

slack = WebClient(token=os.getenv('SLACK_TOKEN'))
slack.chat_postMessage(
    channel='#newsletters',
    text=f"📧 Newsletter Summary\n\n{summary}"
)
```

---

## Non-Gmail Setup

### Using Outlook/Office 365

```env
IMAP_SERVER=outlook.office365.com
SMTP_SERVER=smtp.office365.com
EMAIL_ADDRESS=you@outlook.com
EMAIL_PASSWORD=your-password
```

### Using Yahoo Mail

```env
IMAP_SERVER=imap.mail.yahoo.com
SMTP_SERVER=smtp.mail.yahoo.com
EMAIL_ADDRESS=you@yahoo.com
EMAIL_PASSWORD=your-app-password  # Generate at account.yahoo.com
```

### Using Custom Domain

```env
IMAP_SERVER=imap.yourdomain.com
SMTP_SERVER=smtp.yourdomain.com
```

---

## Troubleshooting

### "Authentication failed"
- **Gmail:** Make sure you're using App Password, not regular password
- **2FA:** App passwords require 2-factor auth to be enabled
- **Less secure apps:** If using old Gmail, enable "less secure apps"

### "No newsletter found today"
- Newsletter might not have arrived yet
- Check `NEWSLETTER_FROM` matches sender exactly
- Try removing `NEWSLETTER_SUBJECT_CONTAINS` to match any subject
- Check your inbox manually to verify it arrived

### "Connection refused"
- Check IMAP/SMTP server addresses
- Gmail: Make sure IMAP is enabled in Gmail settings
- Firewall: Check if port 993 (IMAP) and 465 (SMTP) are open

### "API key invalid"
- Get Anthropic key at: https://console.anthropic.com
- Make sure it starts with `sk-ant-api03-`
- Check for extra spaces in .env file

---

## Output Examples

### Console Output
```
============================================================
Newsletter Summarizer - Starting
Time: 2026-01-13 08:00:15
============================================================
Connecting to imap.gmail.com...
Looking for newsletter from: crew@morningbrew.com

Found email:
  From: Morning Brew <crew@morningbrew.com>
  Subject: ☕ Your Monday morning briefing
  Date: Mon, 13 Jan 2026 06:00:00 -0500

Generating AI summary...
Summary saved to: output/summaries/2026-01-13_newsletter_summary.txt
Sending summary to you@gmail.com...
✅ Summary sent successfully!

============================================================
Newsletter Summarizer - Completed Successfully!
============================================================
```

### Summary Email You Receive

```
Subject: 📋 Summary: ☕ Your Monday morning briefing

Newsletter Summary
============================================================

Original Newsletter: ☕ Your Monday morning briefing
From: Morning Brew <crew@morningbrew.com>
Date: Mon, 13 Jan 2026 06:00:00 -0500

============================================================

## Key Takeaways

• Markets opened higher as tech earnings exceeded expectations
• Federal Reserve signals potential rate adjustment in Q2
• Major acquisition announced in healthcare sector ($12B deal)
• Oil prices surge 5% on supply concerns
• Consumer confidence index reaches 18-month high

## Main Topics

The newsletter covers three main areas: market performance driven 
by strong tech earnings, monetary policy outlook following Fed 
comments, and significant M&A activity in healthcare. Economic 
indicators suggest continued growth momentum.

## Action Items

• Watch for earnings reports from major tech companies this week
• Monitor Fed speeches for policy guidance
• Review healthcare portfolio exposure given M&A activity
• Consider energy sector positioning amid supply dynamics

============================================================

This summary was automatically generated.
Original newsletter is in your inbox.
```

---

## Cost Breakdown

### Per Newsletter
- Input: ~5,000 tokens (newsletter content)
- Output: ~500 tokens (summary)
- **Cost:** ~$0.10-0.20 per summary

### Monthly (Daily Newsletter)
- 30 summaries × $0.15 average
- **Total:** ~$4.50/month

### Compare to:
- Reading full newsletter: 10-15 minutes daily = 5+ hours/month
- Your time value: If worth $20/hour = $100+ saved
- **ROI:** Massive time savings for $4.50

---

## Privacy & Security

✅ **All local** - Newsletter content never leaves your machine except to Claude API  
✅ **Encrypted** - IMAP/SMTP use SSL/TLS encryption  
✅ **App passwords** - More secure than regular passwords  
✅ **No storage** - Anthropic doesn't store your newsletter content  
✅ **Your data** - All summaries saved locally, you control everything  

---

## Tips & Best Practices

### 1. Test Before Automating
Run manually for a few days to make sure it works consistently

### 2. Set Realistic Schedule
Run 30+ minutes after newsletter typically arrives

### 3. Archive Originals
Set up Gmail filter to auto-archive original after script runs

### 4. Multiple Recipients
Send summaries to your team:
```env
SUMMARY_SEND_TO=you@company.com,team@company.com
```

### 5. Customize Summaries
Adjust the prompt for your needs (investor focus, technical depth, etc.)

---

## FAQ

**Q: Does it work with any email provider?**  
A: Yes! Gmail, Outlook, Yahoo, any IMAP/SMTP server.

**Q: Can I summarize multiple newsletters?**  
A: Yes! Run separate instances with different .env configs.

**Q: What if newsletter arrives at different times?**  
A: Run it multiple times per day, or at the latest possible time.

**Q: Can it handle HTML newsletters?**  
A: Yes, it extracts text from HTML emails automatically.

**Q: What about newsletters with images?**  
A: Text content is extracted. Images are ignored (Claude sees text only).

**Q: Is it safe to give script my email password?**  
A: Use App Passwords (not your real password). Much more secure.

---

## Extending the Script

### Add PDF Export
```bash
pip install markdown fpdf
```

### Add Webhook Notifications
```python
import requests
requests.post('https://your-webhook.com', json={'summary': summary})
```

### Database Storage
```python
import sqlite3
# Store summaries in SQLite for searchability
```

### Web Dashboard
Build a simple Flask app to view all summaries

---

## Support

- Issues: Check troubleshooting section first
- Gmail setup: https://support.google.com/accounts/answer/185833
- Anthropic API: https://console.anthropic.com

---

## License

MIT License - Use freely!

---

**Happy automated reading!** 📧✨
