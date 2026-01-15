# Quick Start (No YouTube API Required)

If you don't have a YouTube API key yet, you can still use the tool by manually providing video IDs.

## Setup (5 minutes)

### 1. Copy and configure your environment file

```bash
cp .env.example .env
```

Edit `.env` and add at minimum:

```env
YOUTUBE_PLAYLIST_ID=PLGaYlBJIOoa_vIH-o9MQZHg86xdx496BW
ANTHROPIC_API_KEY=your_key_here
EMAIL_TO=your_email@example.com
```

**Required immediately:**
- `ANTHROPIC_API_KEY` - Get from https://console.anthropic.com/ (you'll need to add a payment method, costs ~$0.10 per video)
- `EMAIL_TO` - Where to send summaries

**Email settings (optional for testing):**
- You can skip email settings and use `--no-email` flag to test
- Add SMTP settings later when ready

### 2. Get a video ID from your playlist

**Option A: Use the helper script**

```bash
python3 get_video_id.py
```

Then paste a YouTube video URL when prompted.

**Option B: Manually extract from URL**

1. Open https://www.youtube.com/playlist?list=PLGaYlBJIOoa_vIH-o9MQZHg86xdx496BW
2. Click the first video (latest one)
3. Copy the video ID from the URL (the part after `v=`)

Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
Video ID is: `dQw4w9WgXcQ`

### 3. Run the tool

```bash
# Test without sending email (recommended first time)
python3 main.py --video-id YOUR_VIDEO_ID --no-email

# Check the output in the summaries/ folder
```

## Example: Complete First Run

```bash
# 1. Set up environment (do this once)
cp .env.example .env
nano .env  # or use your preferred editor

# 2. Get video ID (example)
python3 get_video_id.py
# Paste: https://www.youtube.com/watch?v=8bNwRCLUMvY
# Output: Video ID: 8bNwRCLUMvY

# 3. Run the tool
python3 main.py --video-id 8bNwRCLUMvY --no-email

# 4. Check the output
ls -la summaries/
cat summaries/summary_*.json
```

## What Happens

1. ✅ Extracts video transcript (no download, just text)
2. ✅ Sends to Claude for macro trading analysis
3. ✅ Generates comprehensive summary with:
   - Executive summary
   - Key macro indicators discussed
   - Market outlook and positioning
   - Central bank policy commentary
   - Risks and catalysts
   - Actionable takeaways
4. ✅ Saves to `summaries/` and `transcripts/` folders
5. 📧 Sends email (if configured and not using `--no-email`)

## Cost Per Video

- Anthropic API: ~$0.04-$0.12 per video
- That's it! (YouTube Data API is free if you add it later)

## Add Email Later

Once you're happy with the summaries, set up email:

### For Gmail:

1. Enable 2-Factor Authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Create an app password for "Mail"
4. Add to `.env`:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@example.com
```

5. Test: `python3 main.py --test-email`

## Get YouTube API Key (Optional but Recommended)

For automatic playlist monitoring without manual video IDs:

1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create credentials → API Key
5. Add to `.env`:

```env
YOUTUBE_API_KEY=your_api_key_here
```

6. Now you can run without `--video-id`:

```bash
python3 main.py  # Automatically fetches latest video!
```

## Automate with GitHub Actions

Once everything works locally:

1. Push repo to GitHub
2. Add secrets in repo Settings → Secrets and variables → Actions
3. The workflow runs daily at 9 AM UTC automatically

See [README.md](README.md) for full GitHub Actions setup.

## Troubleshooting

### "No module named 'anthropic'"
```bash
pip3 install -r requirements.txt
```

### "Missing required environment variables"
Make sure `.env` has at least:
- `YOUTUBE_PLAYLIST_ID`
- `ANTHROPIC_API_KEY`
- `EMAIL_TO`

### "Could not extract transcript"
The video may not have captions. Try a different video from the playlist.

### "SMTP authentication failed"
Either:
- Use `--no-email` flag to skip email for now, OR
- Set up Gmail App Password (see above)

## Daily Workflow Without YouTube API

If you prefer not to get a YouTube API key:

```bash
# Each day:
# 1. Check playlist for new video
# 2. Get video ID
python3 get_video_id.py

# 3. Run summary
python3 main.py --video-id VIDEO_ID
```

Or create a shell script:

```bash
#!/bin/bash
# daily_summary.sh
echo "Paste video URL:"
read url
video_id=$(echo "$url" | grep -oP '(?<=v=)[^&]+')
python3 main.py --video-id "$video_id"
```

## Need Help?

- Full documentation: [README.md](README.md)
- Detailed setup: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- File an issue: https://github.com/yourusername/TheGreatInformationGatherer/issues
