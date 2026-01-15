# Bloomberg Shows Scheduling Guide

This guide explains how to process multiple Bloomberg shows on different schedules.

## Quick Start

### 1. List Available Shows

```bash
python3 process_show.py --list
```

### 2. Process a Single Show Manually

```bash
# Process Bloomberg Brief
python3 process_show.py bloomberg_brief

# Process without sending email
python3 process_show.py bloomberg_brief --no-email

# Force reprocess even if already done
python3 process_show.py bloomberg_brief --force
```

### 3. View Schedule

```bash
python3 show_schedule.py
```

This shows when each show publishes and generates cron entries for automation.

## Configuration

Edit [shows_config.yaml](shows_config.yaml) to add or modify shows:

```yaml
shows:
  your_show_key:
    name: "Show Display Name"
    playlist_id: "YouTube_Playlist_ID"
    state_file: ".last_processed_your_show"
    publish_schedule:
      days: ["monday", "tuesday", "wednesday", "thursday", "friday"]
      time: "14:00"  # When show typically publishes (24-hour format)
      timezone: "America/New_York"
    fetch_delay_minutes: 30  # Wait 30 min after publish before fetching
    enabled: true
```

## Finding Playlist IDs

Use the helper script to find Bloomberg show playlist IDs:

```bash
# Interactive search
python3 find_playlist_ids.py

# Direct search
python3 find_playlist_ids.py "Bloomberg Surveillance"
```

## Automation Options

### Option 1: Local Cron (Mac/Linux)

1. Run `python3 show_schedule.py` to generate cron entries
2. Edit your crontab: `crontab -e`
3. Paste the generated cron lines (update paths)
4. Save and exit

Example cron entry:
```bash
30 13 * * 1-5 cd /path/to/repo && /usr/bin/python3 process_show.py bloomberg_brief
```

### Option 2: GitHub Actions (Cloud-based)

Create workflow files in `.github/workflows/`:

**Example: `.github/workflows/bloomberg-brief.yml`**
```yaml
name: Bloomberg Brief Daily Summary

on:
  schedule:
    - cron: '30 13 * * 1-5'  # Mon-Fri at 1:30 PM UTC
  workflow_dispatch:  # Allow manual trigger

jobs:
  process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Process Bloomberg Brief
        env:
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          SMTP_SERVER: ${{ secrets.SMTP_SERVER }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
          SMTP_USERNAME: ${{ secrets.SMTP_USERNAME }}
          SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
          EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
        run: python3 process_show.py bloomberg_brief

      - name: Commit state file
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .last_processed_*
          git diff --quiet && git diff --staged --quiet || git commit -m "Update processed state"
          git push
```

Add separate workflow files for each show with different schedules.

### Option 3: Manual with Scripts

Run shows manually when needed:

```bash
# Process all enabled shows
for show in bloomberg_brief bloomberg_surveillance bloomberg_markets; do
  python3 process_show.py $show
done
```

## Email Behavior

**Individual emails (default):** Each show sends its own email immediately after processing.

**Daily digest (alternative):** Configure in `shows_config.yaml`:
```yaml
email:
  send_individual: false
  send_daily_digest: true
  digest_time: "18:00"
  digest_timezone: "America/New_York"
```

## Best Practices

1. **Stagger fetch times** - Don't fetch all shows at once to spread API usage
2. **Add delays** - Wait 30-60 minutes after publish time to ensure video is fully processed
3. **Test first** - Use `--no-email` flag when testing new shows
4. **Check schedules** - Bloomberg may change publish times; update config as needed
5. **Monitor state files** - `.last_processed_*` files track what's been processed

## Troubleshooting

**Show already processed:**
```bash
python3 process_show.py bloomberg_brief --force
```

**Can't find video:**
- Check playlist ID is correct
- Verify show published today
- Try increasing `fetch_delay_minutes`

**Email not sending:**
- Verify SMTP credentials in `.env`
- Test with: `python3 main.py --test-email`
- Use `--no-email` to skip and just generate summaries

## Cost Estimates

Per video processing:
- YouTube API: ~1-3 quota units (10,000 free daily)
- Claude API: ~$0.05-$0.15 per video
- 3 shows daily: ~$4.50-$13.50/month

## Example Workflow

1. **Morning**: Bloomberg Brief processes at 1:30 PM UTC (8:30 AM ET)
2. **Midday**: Bloomberg Surveillance at 3:00 PM UTC (10:00 AM ET)
3. **Afternoon**: Bloomberg Markets at 6:30 PM UTC (1:30 PM ET)
4. **Result**: Receive 3 separate emails throughout the day with latest summaries
