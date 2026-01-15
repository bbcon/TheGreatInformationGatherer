# The Great Information Gatherer

An automated tool that extracts transcripts from YouTube videos, generates AI-powered macro trading summaries using Claude, and delivers them via email. Designed for global macro traders who need daily intelligence from market commentary videos.

## Features

- **No API Keys Required**: Uses yt-dlp to fetch playlists and transcripts - completely free!
- **Automated Daily Summaries**: GitHub Actions runs daily to process the latest video
- **Reliable Transcript Extraction**: Dual-method approach (youtube-transcript-api + yt-dlp fallback)
- **AI-Powered Analysis**: Claude generates comprehensive summaries focused on:
  - Key macro economic indicators
  - Market outlook and positioning recommendations
  - Central bank policy developments
  - Risk factors and catalysts
  - Actionable trading insights
- **Email Delivery**: Automated email delivery with formatted HTML summaries
- **State Management**: Tracks processed videos to avoid duplicates

## Quick Start

**⚡ New user?** Start with [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup without YouTube API key!

### Prerequisites

- Python 3.9 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/)) - **Required** (only real cost: ~$0.05-$0.15/video)
- Email account with SMTP access (Gmail, Outlook, etc.) - Optional for testing

**Note**: YouTube API key is NOT required - yt-dlp handles everything for free!

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/TheGreatInformationGatherer.git
   cd TheGreatInformationGatherer
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your credentials:
   ```env
   # YouTube Configuration
   YOUTUBE_PLAYLIST_ID=PLGaYlBJIOoa_vIH-o9MQZHg86xdx496BW
   YOUTUBE_API_KEY=your_youtube_api_key  # Optional but recommended

   # Anthropic API
   ANTHROPIC_API_KEY=your_anthropic_api_key

   # Email Configuration (for Gmail)
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password  # See Gmail setup below
   EMAIL_FROM=your_email@gmail.com
   EMAIL_TO=recipient@example.com
   ```

### Gmail Setup

For Gmail users, you'll need to use an **App Password** instead of your regular password:

1. Enable 2-Factor Authentication on your Google account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Use this 16-character password in your `.env` file as `SMTP_PASSWORD`

### Usage

#### Run Manually

```bash
# Process latest video and send email
python3 main.py

# Process a specific video by ID
python3 main.py --video-id VIDEO_ID

# Generate summary without sending email
python3 main.py --no-email

# Force reprocessing of already-processed video
python3 main.py --force

# Test email configuration
python3 main.py --test-email
```

#### Set Up Automated Daily Runs

The repository includes a GitHub Actions workflow that runs automatically.

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial setup"
   git push origin main
   ```

2. **Add GitHub Secrets**

   Go to your repository Settings → Secrets and variables → Actions, and add:

   - `YOUTUBE_PLAYLIST_ID` - Your YouTube playlist ID
   - `YOUTUBE_API_KEY` - YouTube Data API key (optional)
   - `ANTHROPIC_API_KEY` - Your Anthropic API key
   - `SMTP_SERVER` - SMTP server (e.g., smtp.gmail.com)
   - `SMTP_PORT` - SMTP port (e.g., 587)
   - `SMTP_USERNAME` - Your email address
   - `SMTP_PASSWORD` - Your email app password
   - `EMAIL_FROM` - Sender email address
   - `EMAIL_TO` - Recipient email address

3. **Configure Schedule**

   Edit [.github/workflows/daily-summary.yml](.github/workflows/daily-summary.yml) to adjust the run time:
   ```yaml
   schedule:
     - cron: '0 9 * * *'  # 9:00 AM UTC daily
   ```

4. **Manual Trigger**

   You can also manually trigger the workflow from the Actions tab in GitHub.

## Project Structure

```
TheGreatInformationGatherer/
├── main.py                          # Main orchestration script
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variable template
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── .github/
│   └── workflows/
│       └── daily-summary.yml        # GitHub Actions workflow
├── src/
│   ├── __init__.py
│   ├── youtube_handler.py           # YouTube transcript extraction
│   ├── summarizer.py                # AI summary generation
│   └── email_sender.py              # Email delivery
├── summaries/                       # Generated summaries (auto-created)
└── transcripts/                     # Extracted transcripts (auto-created)
```

## How It Works

1. **Fetch Latest Video**: Queries the YouTube playlist to find the most recent video
2. **Extract Transcript**: Downloads the video transcript (no audio/video download)
3. **Check if Processed**: Compares with `.last_processed_video` to avoid duplicates
4. **Generate Summary**: Sends transcript to Claude with macro trading-focused prompt
5. **Format Email**: Converts markdown summary to HTML email
6. **Send Email**: Delivers formatted summary via SMTP
7. **Save Records**: Stores transcript and summary as JSON files
8. **Update State**: Marks video as processed

## Customization

### Modify Summary Focus

Edit the `SUMMARY_PROMPT` in [src/summarizer.py](src/summarizer.py) to adjust what the AI focuses on.

### Change Email Template

Modify `format_email_body()` in [src/summarizer.py](src/summarizer.py) to customize email formatting.

### Add Multiple Recipients

You can modify the email sending logic in [main.py](main.py) to support multiple recipients:

```python
email_to_list = config['email_to'].split(',')
for recipient in email_to_list:
    sender.send_summary_with_video_data(...)
```

### Use Different AI Models

Change the model in [src/summarizer.py](src/summarizer.py):

```python
def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
```

Available models:
- `claude-3-5-sonnet-20241022` (default, best balance)
- `claude-opus-4-5-20251101` (highest quality)
- `claude-3-5-haiku-20241022` (fastest, cheapest)

## Troubleshooting

### "Could not fetch latest video ID"

- **Solution 1**: Add a YouTube Data API key to your `.env` file
- **Solution 2**: Use `--video-id` flag to specify video manually
- **Solution 3**: Check that the playlist is public and the ID is correct

### "Transcripts are disabled for video"

The video doesn't have captions available. Some videos don't provide transcripts.

### Email authentication fails

- For Gmail: Make sure you're using an App Password, not your regular password
- For other providers: Check SMTP server and port settings
- Run `python3 main.py --test-email` to diagnose issues

### GitHub Actions fails

- Check that all secrets are properly set in repository settings
- Review the Actions logs for specific error messages
- Ensure the repository has write permissions for committing state

## Cost Estimates

### Anthropic API

Approximate costs per video (using Claude 3.5 Sonnet):
- Transcript input: ~2,000-8,000 tokens ($0.02-$0.08)
- Summary output: ~1,000-2,000 tokens ($0.02-$0.04)
- **Total per video: $0.04-$0.12**

Daily usage: ~$1.20-$3.60/month

### YouTube Data API

- Free tier: 10,000 quota units/day
- Playlist lookup: 1 unit per request
- More than sufficient for daily use

## Extending the Tool

### Add More Data Sources

You can extend this tool to gather information from multiple sources:
- Multiple YouTube playlists
- Podcast transcripts
- News articles
- Financial reports

### Integration with Trading Systems

The summaries are saved as JSON files in the `summaries/` directory, making it easy to:
- Parse and extract specific data points
- Feed into trading algorithms
- Build a database of historical market commentary
- Perform sentiment analysis over time

### Historical Analysis

Process historical videos:
```bash
for video_id in VIDEO_ID_1 VIDEO_ID_2 VIDEO_ID_3; do
  python3 main.py --video-id $video_id --no-email
done
```

## Contributing

Feel free to open issues or submit pull requests for improvements!

## License

MIT License - feel free to use this for your trading operations.

## Disclaimer

This tool is for informational purposes only. The summaries generated are based on publicly available video content and should not be considered financial advice. Always do your own research before making trading decisions.
