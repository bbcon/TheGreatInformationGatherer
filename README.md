# The Daily Macro & Market Brief

Automated system that extracts transcripts from Bloomberg TV shows, generates AI-powered macro summaries, and delivers polished daily/weekly briefs via email.

## What It Does

1. **Extracts transcripts** from YouTube (Bloomberg Surveillance, Daybreak Europe, The Close, etc.)
2. **Summarizes each show** using Claude AI with macro-focused prompts
3. **Generates daily briefs** combining all show summaries into one coherent narrative
4. **Generates weekly briefs** synthesizing the week's key themes
5. **Generates monthly briefs** cutting through the noise to highlight what really mattered
6. **Sends styled HTML emails** with professional formatting

## Project Structure

```
TheGreatInformationGatherer/
│
├── process_show.py           # Process a single Bloomberg show
├── generate_daily_brief.py   # Generate daily brief from show summaries
├── generate_weekly_brief.py  # Generate weekly brief from daily briefs
├── generate_monthly_brief.py # Generate monthly brief from weekly briefs
├── send_briefs.py            # Send styled HTML emails
├── process_knowledge.py     # Process knowledge documents for context
├── main.py                  # Legacy single-video processor
│
├── shows_config.yaml        # Show definitions (playlists, prompts)
├── config.yaml              # General configuration
│
├── src/                     # Core modules
│   ├── youtube_handler.py   # YouTube transcript extraction (yt-dlp)
│   ├── summarizer.py        # Claude AI summarization
│   ├── email_sender.py      # SMTP email delivery
│   └── output_handler.py    # File output management
│
├── scripts/                 # Utility scripts
│   ├── find_playlist_ids.py # Find YouTube playlist IDs
│   ├── process_historical.py # Batch process historical videos
│   └── show_schedule.py     # Display show schedules
│
├── summaries/               # Generated content
│   ├── _daily_briefs/       # Daily macro briefs (markdown)
│   ├── _weekly_briefs/      # Weekly macro briefs (markdown)
│   ├── _monthly_briefs/     # Monthly macro briefs (markdown)
│   ├── bloomberg_surveillance/
│   ├── daybreak_europe/
│   └── ...
│
├── transcripts/             # Raw YouTube transcripts (JSON)
├── state/                   # Processing state files
├── substack/                # Newsletter assets (logos, templates)
├── knowledge/               # Reference documents for AI context
│
└── docs/                    # Documentation
    └── SETUP.md             # Complete setup guide
```

## Quick Start

```bash
# Install
pip3 install -r requirements.txt
cp .env.example .env  # Add your ANTHROPIC_API_KEY

# Process a show
python3 process_show.py --show bloomberg_surveillance

# Generate daily brief
python3 generate_daily_brief.py --date 2026-01-30

# Generate weekly brief
python3 generate_weekly_brief.py --week 2026-W05

# Generate monthly brief
python3 generate_monthly_brief.py --month 2026-01

# Send via email
python3 send_briefs.py --daily 2026-01-30
python3 send_briefs.py --weekly 2026-W05
```

## Key Scripts

| Script | Purpose |
|--------|---------|
| `process_show.py` | Fetch transcript and generate summary for one show |
| `generate_daily_brief.py` | Combine show summaries into daily brief |
| `generate_weekly_brief.py` | Synthesize daily briefs into weekly themes |
| `generate_monthly_brief.py` | Synthesize weekly briefs into monthly overview (~1500 words) |
| `send_briefs.py` | Send HTML-styled briefs via email |
| `main.py` | Legacy script for single video processing |

## Configuration

**Environment variables** (`.env`):
```env
ANTHROPIC_API_KEY=your_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@example.com
```

**Shows** (`shows_config.yaml`):
```yaml
shows:
  bloomberg_surveillance:
    playlist_id: PLIilwIraDV2LQHeTYrboyJ7VGzGImXjoz
    schedule_time: "14:00"
    # ...
```

See `docs/SETUP.md` for complete setup instructions.

## Website

The project includes a static website to browse all briefs:

```bash
# Sync briefs to website format
python3 sync_to_website.py

# Preview locally (requires Ruby/Jekyll)
cd website && bundle install && bundle exec jekyll serve

# Open http://localhost:4000
```

The website automatically deploys to GitHub Pages when you push changes to `main`.

## Cost

- **Anthropic API**: ~$0.05-0.15 per show summary
- **Daily (5 shows + brief)**: ~$0.30-0.50
- **Monthly**: ~$10-15
- **YouTube**: Free (uses yt-dlp, no API key needed)

## License

MIT
