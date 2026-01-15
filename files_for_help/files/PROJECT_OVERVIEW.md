# Bloomberg Markets Summarizer - Project Overview

## What This Does

Automatically fetches Bloomberg's daily markets video, transcribes it, and generates AI-powered summaries with key market insights every morning.

## Features

### Core Functionality
- ✅ Fetches latest Bloomberg Markets video from YouTube
- ✅ Downloads and extracts audio
- ✅ Transcribes using Whisper (local or API)
- ✅ Generates structured summaries using Claude or GPT
- ✅ Runs automatically on schedule via cron
- ✅ Archives historical summaries
- ✅ Comprehensive logging

### Output Includes
- Executive summary (2-3 sentences)
- Market movements (indices, currencies, commodities)
- Top stories (3-5 key items)
- Economic data releases
- Notable quotes from analysts
- Forward-looking outlook

## Architecture

```
bloomberg-markets-summarizer/
├── main.py                    # Main orchestration script
├── config.yaml               # Configuration settings
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
│
├── src/
│   ├── video_fetcher.py     # YouTube video fetching
│   ├── transcriber.py       # Audio transcription (Whisper)
│   ├── summarizer.py        # AI summarization (Claude/GPT)
│   └── utils.py             # Helper functions
│
├── output/
│   ├── latest_summary.md    # Most recent summary
│   ├── summaries/           # Historical summaries
│   └── transcripts/         # Full transcripts
│
├── logs/                     # Application logs
└── temp/                     # Temporary audio files
```

## Technology Stack

### Core Dependencies
- **yt-dlp**: YouTube video/audio downloading
- **ffmpeg**: Audio processing
- **whisper**: Speech-to-text transcription
- **anthropic/openai**: AI-powered summarization

### Optional Features
- SendGrid for email notifications
- PDF generation support
- Slack/Telegram integration

## Workflow

```
1. Cron triggers at 7 AM daily
        ↓
2. Fetch latest Bloomberg video
        ↓
3. Download and extract audio
        ↓
4. Transcribe with Whisper
        ↓
5. Generate AI summary
        ↓
6. Save to output/latest_summary.md
        ↓
7. Clean up old files
        ↓
8. (Optional) Send notifications
```

## Configuration Options

### Video Source
```yaml
video:
  source_url: "https://www.youtube.com/@markets/videos"
  title_keywords: ["Bloomberg Markets", "The Close"]
  max_age_hours: 24
```

### Transcription
```yaml
transcription:
  model: "base"              # Whisper model size
  use_api: false             # Use OpenAI API vs local
```

### Summary Generation
```yaml
summary:
  provider: "anthropic"      # or "openai"
  model: "claude-sonnet-4-20250514"
  detail_level: "concise"    # brief/concise/detailed
  focus_areas:
    - "Equity markets"
    - "Bond yields"
    - "Currency movements"
```

### Scheduling
```yaml
schedule:
  time: "07:00"
  timezone: "America/New_York"
```

## API Keys Required

### Option 1: Anthropic Claude (Recommended)
- Sign up at: https://console.anthropic.com
- Get API key from dashboard
- Best for: High-quality financial analysis

### Option 2: OpenAI
- Sign up at: https://platform.openai.com
- Get API key from dashboard
- Best for: Using Whisper API for transcription

### Both Options
Use both APIs for optimal results:
- OpenAI Whisper API: Fast transcription
- Anthropic Claude: High-quality summaries

## Installation

### Quick Install
```bash
git clone <repo-url>
cd bloomberg-markets-summarizer
./install.sh
```

### Manual Install
```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env

# Test
python3 test_setup.py

# Run
python3 main.py

# Schedule
python3 setup_cron.py
```

## Customization Examples

### Focus on Tech Stocks
```yaml
summary:
  focus_areas:
    - "Technology sector"
    - "Semiconductor industry"
    - "AI and cloud computing"
    - "Mega-cap tech earnings"
```

### Brief Morning Briefing
```yaml
summary:
  detail_level: "brief"
  include_sections:
    - executive_summary
    - market_movements
    - top_stories
```

### Detailed Research Report
```yaml
summary:
  detail_level: "detailed"
  max_tokens: 4000
  include_sections:
    - executive_summary
    - market_movements
    - top_stories
    - economic_data
    - sector_analysis
    - technical_analysis
    - notable_quotes
    - outlook
```

## Output Format

### Markdown Summary Structure
```markdown
# Bloomberg Markets Summary
**Date:** 2025-01-13
**Video:** Bloomberg Markets: The Close
**Generated:** 2025-01-13 07:15:30

---

## Executive Summary
[2-3 sentence overview]

## Market Movements
[Indices, currencies, commodities with data]

## Top Stories
[3-5 key items with details]

## Economic Data
[Releases and implications]

## Notable Quotes
[Key insights from analysts]

## Outlook
[What to watch for]

---
*Auto-generated from Bloomberg Markets video*
```

## Error Handling

### Common Issues

1. **"No suitable video found"**
   - Bloomberg hasn't uploaded yet
   - Run later in day (after 4 PM ET)

2. **"FFmpeg not found"**
   - Install: `sudo apt-get install ffmpeg`

3. **"API rate limit"**
   - Check API usage dashboard
   - Consider caching transcripts

4. **"Transcription fails"**
   - Check audio file exists
   - Try using OpenAI API: `use_api: true`

### Logging

All operations logged to:
- `logs/bloomberg_summarizer.log` - Application logs
- `logs/cron.log` - Scheduled run logs

View logs:
```bash
tail -f logs/bloomberg_summarizer.log
```

## Performance

### Typical Run Times
- Video fetch: 10-30 seconds
- Audio download: 30-60 seconds
- Transcription (local): 2-5 minutes
- Transcription (API): 30-60 seconds
- Summary generation: 10-30 seconds

**Total**: 3-7 minutes (local) or 2-3 minutes (API)

### Resource Usage
- Disk: ~100MB per video (temporary)
- Memory: 1-4GB (depending on Whisper model)
- CPU: Moderate during transcription

## Maintenance

### Regular Tasks
- Monitor logs weekly
- Check API usage monthly
- Clean old files (automated)
- Update dependencies quarterly

### Updates
```bash
git pull
pip install -r requirements.txt --upgrade
```

## Security Considerations

- API keys stored in `.env` (gitignored)
- No sensitive data logged
- Temporary files cleaned up
- Cron runs as user (not root)

## Future Enhancements

Potential additions:
- [ ] Multi-source support (CNBC, Fox Business)
- [ ] Sentiment analysis
- [ ] Chart/graph generation
- [ ] Mobile app integration
- [ ] Real-time alerts
- [ ] Portfolio impact analysis
- [ ] Compare to analyst forecasts

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests if applicable
4. Submit pull request

## License

MIT License - See LICENSE file

## Support

- GitHub Issues: <repo-url>/issues
- Documentation: README.md, QUICKSTART.md
- Logs: `logs/` directory

## Credits

Built with:
- yt-dlp by youtube-dl team
- OpenAI Whisper
- Anthropic Claude
- Bloomberg Markets content

## Disclaimer

This tool is for personal use. Bloomberg content is subject to their terms of service. Summaries are AI-generated and should not be the sole basis for investment decisions.

---

**Happy trading!** 📈
