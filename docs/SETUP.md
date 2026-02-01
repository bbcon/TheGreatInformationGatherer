# Setup Guide

## Prerequisites

- Python 3.9+
- Anthropic API key ([get one here](https://console.anthropic.com/))
- Gmail account with App Password (for email delivery)

**Note**: YouTube API key is NOT required - yt-dlp handles everything for free.

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
git clone https://github.com/yourusername/TheGreatInformationGatherer.git
cd TheGreatInformationGatherer
pip3 install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key

# Email (Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@example.com
```

### 3. Gmail App Password

1. Enable 2-Factor Authentication on your Google account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Use this 16-character password as `SMTP_PASSWORD`

### 4. Test It

```bash
# Process a specific show
python3 process_show.py --show bloomberg_surveillance

# Generate daily brief from all show summaries
python3 generate_daily_brief.py

# Send the brief via email
python3 send_briefs.py --daily 2026-01-30
```

## GitHub Actions (Automated Daily Runs)

### Add Repository Secrets

Go to Settings → Secrets and variables → Actions:

- `ANTHROPIC_API_KEY`
- `SMTP_SERVER` (smtp.gmail.com)
- `SMTP_PORT` (587)
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `EMAIL_FROM`
- `EMAIL_TO`

### Workflow Schedule

Workflows are configured in `.github/workflows/`:

| Show | Time (CET) | File |
|------|------------|------|
| Daybreak Europe | 10:30 | `daybreak-europe.yml` |
| Bloomberg Surveillance | 15:00 | `bloomberg-surveillance.yml` |
| The China Show | 05:00 | `china-show.yml` |
| The Close | 22:30 | `the-close.yml` |
| Bloomberg Brief | 08:00 | `bloomberg-brief.yml` |
| Daily Summary | 23:00 | `daily-summary.yml` |

## Cost Estimates

### Anthropic API (~$0.05-0.15 per video)

- Input: ~2,000-8,000 tokens ($0.02-$0.08)
- Output: ~1,000-2,000 tokens ($0.02-$0.04)
- Daily (5 shows): ~$0.25-$0.75
- Monthly: ~$7.50-$22.50

### YouTube API

Not required - yt-dlp is free and has no quotas.
