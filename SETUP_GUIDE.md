# Quick Setup Guide

## Step 1: Configure Environment Variables

Create your `.env` file from the template:

```bash
cp .env.example .env
```

Then edit `.env` and fill in your credentials:

```env
# YouTube Configuration
YOUTUBE_PLAYLIST_ID=PLGaYlBJIOoa_vIH-o9MQZHg86xdx496BW

# Get your Anthropic API key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-...

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@example.com

# Optional: Get YouTube API key from: https://console.cloud.google.com/apis/credentials
YOUTUBE_API_KEY=AIza...
```

## Step 2: Gmail App Password Setup

If using Gmail, you need an App Password:

1. Go to your Google Account: https://myaccount.google.com/
2. Select **Security**
3. Under "Signing in to Google," select **2-Step Verification** (enable if not already)
4. At the bottom, select **App passwords**
5. Select app: **Mail**
6. Select device: **Other (Custom name)** → "The Great Information Gatherer"
7. Click **Generate**
8. Copy the 16-character password (spaces are optional)
9. Use this password as `SMTP_PASSWORD` in your `.env` file

## Step 3: Get Anthropic API Key

1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Go to **API Keys** section
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-api03-...`)
6. Add to `.env` as `ANTHROPIC_API_KEY`

## Step 4: (Optional) Get YouTube API Key

While optional, this is recommended for reliable playlist access:

1. Go to https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable **YouTube Data API v3**
4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy the key and add to `.env` as `YOUTUBE_API_KEY`

## Step 5: Test Your Setup

```bash
# Test email configuration
python3 main.py --test-email

# Test full workflow without sending email
python3 main.py --no-email

# Run complete workflow
python3 main.py
```

## Step 6: Set Up GitHub Actions (Optional)

For automated daily summaries:

1. Push repository to GitHub
2. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add each of these:
   - `YOUTUBE_PLAYLIST_ID`
   - `ANTHROPIC_API_KEY`
   - `SMTP_SERVER`
   - `SMTP_PORT`
   - `SMTP_USERNAME`
   - `SMTP_PASSWORD`
   - `EMAIL_FROM`
   - `EMAIL_TO`
   - `YOUTUBE_API_KEY` (optional)

4. The workflow will automatically run daily at 9 AM UTC
5. You can also trigger it manually from the **Actions** tab

## Troubleshooting

### Error: "Missing required environment variables"
- Make sure your `.env` file exists and has all required variables
- Check for typos in variable names

### Error: "SMTP authentication failed"
- For Gmail, ensure you're using an App Password, not your regular password
- Verify 2-Factor Authentication is enabled on your Google account
- Double-check the password has no spaces or typos

### Error: "Could not fetch latest video ID"
- Add a YouTube API key to your `.env` file, OR
- Use `--video-id` flag with a specific video ID: `python3 main.py --video-id dQw4w9WgXcQ`

### Error: "Transcripts are disabled for video"
- The video doesn't have captions/subtitles available
- Try a different video from the playlist

## Cost Estimates

- **Anthropic API**: ~$0.04-$0.12 per video (~$3.60/month for daily use)
- **YouTube API**: Free (10,000 quota units/day, we use 1 per day)
- **GitHub Actions**: Free (2,000 minutes/month for public repos)

## What Happens When You Run It

1. Fetches the latest video from the YouTube playlist
2. Checks if it's already been processed (stored in `.last_processed_video`)
3. Extracts the transcript (no video download!)
4. Sends transcript to Claude for analysis
5. Generates macro trading-focused summary
6. Formats as HTML email
7. Sends to your configured email address
8. Saves transcript and summary as JSON files in `transcripts/` and `summaries/`
9. Updates `.last_processed_video` to prevent duplicates

## Next Steps

- Customize the summary prompt in `src/summarizer.py` for your specific needs
- Add multiple email recipients in `main.py`
- Process historical videos: `python3 main.py --video-id VIDEO_ID --no-email`
- Integrate with your trading systems by parsing the JSON outputs
