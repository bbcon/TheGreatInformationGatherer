# Bloomberg Markets Daily Summarizer

Automated system to fetch, transcribe, and summarize Bloomberg's daily markets video, delivering key insights every morning.

## 💰 Cost: ~$3-9/month (or FREE trial!)

- **FREE:** YouTube auto-captions for transcription (no API key needed!)
- **Cheap:** AI summarization only (~$0.10-0.30/day)
- **Just ONE API key needed** (Anthropic Claude)

See [BUDGET_SETUP.md](BUDGET_SETUP.md) for full cost breakdown and free options.

## Features

- Fetches the latest Bloomberg Markets video
- Extracts audio and transcribes content
- Generates AI-powered summaries with key insights
- Runs automatically via cron job
- Outputs clean, actionable summaries

## Setup

### Prerequisites

```bash
# Python 3.8+
python --version

# Install system dependencies
sudo apt-get update
sudo apt-get install -y ffmpeg
```

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd bloomberg-markets-summarizer
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API keys in `.env`:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Set up the daily cron job:
```bash
# Run setup script
python setup_cron.py

# Or manually add to crontab (runs at 7 AM daily):
crontab -e
# Add: 0 7 * * * cd /path/to/bloomberg-markets-summarizer && /usr/bin/python3 main.py >> logs/cron.log 2>&1
```

## Usage

### Manual Run
```bash
python main.py
```

### Check Latest Summary
```bash
cat output/latest_summary.md
# Or
cat output/summaries/YYYY-MM-DD_summary.md
```

### View Logs
```bash
tail -f logs/bloomberg_summarizer.log
```

## Configuration

Edit `config.yaml` to customize:
- Summary length and detail level
- Output format preferences
- Video source preferences
- Notification settings

## Output Structure

```
output/
├── latest_summary.md          # Most recent summary (symlink)
├── summaries/                 # Historical summaries
│   ├── 2025-01-13_summary.md
│   └── 2025-01-14_summary.md
└── transcripts/               # Full transcripts
    ├── 2025-01-13_transcript.txt
    └── 2025-01-14_transcript.txt
```

## Summary Format

Each summary includes:
1. **Executive Summary** - 2-3 sentence overview
2. **Market Movements** - Key indices, currencies, commodities
3. **Top Stories** - Major market-moving news
4. **Economic Data** - Important releases and indicators
5. **Notable Quotes** - Key insights from analysts
6. **Outlook** - What to watch for

## Troubleshooting

### Video not found
- Bloomberg may have changed their URL structure
- Check `video_fetcher.py` and update selectors

### Transcription fails
- Verify ffmpeg is installed: `ffmpeg -version`
- Check audio extraction in `transcriber.py`

### API rate limits
- Adjust wait times in `config.yaml`
- Consider caching transcripts

## License

MIT License

## Contributing

Pull requests welcome! Please ensure code passes linting:
```bash
flake8 .
black .
```
