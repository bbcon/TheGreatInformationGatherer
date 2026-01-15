# Quick Start Guide

Get your Bloomberg Markets summarizer up and running in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- ffmpeg (for audio processing)
- API key from Anthropic or OpenAI

## Installation Steps

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg python3-pip
```

**macOS:**
```bash
brew install ffmpeg python3
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd bloomberg-markets-summarizer

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your favorite editor
nano .env
```

Add your API key:
```
ANTHROPIC_API_KEY=sk-ant-api03-...
# OR
OPENAI_API_KEY=sk-...
```

### 4. Test Your Setup

```bash
python test_setup.py
```

This will verify:
- ✓ All dependencies installed
- ✓ API keys configured
- ✓ ffmpeg available
- ✓ Directories created

### 5. Run Your First Summary

```bash
python main.py
```

The script will:
1. Find the latest Bloomberg Markets video
2. Download and transcribe it
3. Generate an AI summary
4. Save to `output/latest_summary.md`

### 6. Setup Daily Automation

```bash
python setup_cron.py
```

This creates a cron job that runs every morning at 7 AM.

## View Your Summary

```bash
# View latest summary
cat output/latest_summary.md

# Or open in your browser
# The summary is in markdown format
```

## Customization

Edit `config.yaml` to customize:

```yaml
# Change summary detail level
summary:
  detail_level: "detailed"  # brief, concise, or detailed

# Focus on specific topics
  focus_areas:
    - "Tech stocks"
    - "Cryptocurrency"
    - "Your specific interest"

# Change schedule time
schedule:
  time: "06:30"  # 6:30 AM
```

## Troubleshooting

### "No suitable video found"
- Bloomberg may not have uploaded today's video yet
- Try running later in the day (after 4 PM ET)

### "FFmpeg not found"
```bash
# Install ffmpeg
sudo apt-get install ffmpeg
```

### "API key invalid"
- Check your .env file
- Ensure no extra spaces or quotes
- Verify key starts with `sk-ant-` (Anthropic) or `sk-` (OpenAI)

### "Transcription too slow"
Edit `config.yaml`:
```yaml
transcription:
  use_api: true  # Use OpenAI API instead of local model
```

## Daily Workflow

Once set up, your morning routine:

1. **7:00 AM** - Script runs automatically
2. **7:15 AM** - Summary ready in `output/latest_summary.md`
3. **Read summary** - Get market insights with your morning coffee ☕

## Advanced Usage

### Email Summaries to Yourself

```yaml
# In config.yaml
notifications:
  enabled: true
  methods:
    - email
```

Add SendGrid key to `.env`:
```
SENDGRID_API_KEY=SG.xxx
NOTIFICATION_EMAIL=you@example.com
```

### Save PDFs

```yaml
# In config.yaml
output:
  formats:
    - markdown
    - pdf
```

## Support

- Check logs: `tail -f logs/bloomberg_summarizer.log`
- View cron logs: `tail -f logs/cron.log`
- Issues? Open a GitHub issue with your logs

## Next Steps

- Star the repository ⭐
- Customize for your needs
- Share improvements via pull requests

Happy trading! 📈
