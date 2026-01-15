# GitHub Actions Setup Guide

This guide will help you set up automated daily summaries for all Bloomberg shows using GitHub Actions.

## Schedule Overview (CET/Switzerland Time)

Here's when each workflow runs and when you'll receive emails:

| Show | CET Time | What Happens |
|------|----------|--------------|
| **The China Show** | 07:45 | Morning email from Shanghai markets |
| **Daybreak Europe** | 09:45 | Mid-morning email from European markets |
| **Bloomberg Surveillance** | 14:00-15:00 | Early afternoon email from US morning show |
| **Bloomberg Brief** | 14:30 | Afternoon email with daily brief |
| **The Close** | 22:45 | Late evening email from US market close |

## Setup Steps

### 1. Push Your Code to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial setup with GitHub Actions workflows"

# Add your remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/TheGreatInformationGatherer.git

# Push to GitHub
git push -u origin main
```

### 2. Add Secrets to GitHub Repository

Go to your repository on GitHub:
1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add each of the following secrets:

**Required Secrets:**

| Secret Name | Value | Where to Get It |
|------------|-------|-----------------|
| `YOUTUBE_API_KEY` | Your YouTube Data API key | [Google Cloud Console](https://console.cloud.google.com/) |
| `ANTHROPIC_API_KEY` | Your Claude API key | [Anthropic Console](https://console.anthropic.com/) |
| `SMTP_SERVER` | SMTP server address | Gmail: `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port | Gmail: `587` |
| `SMTP_USERNAME` | Your email address | Your Gmail address |
| `SMTP_PASSWORD` | Email app password | [Gmail App Passwords](https://myaccount.google.com/apppasswords) |
| `EMAIL_FROM` | Sender email | Same as SMTP_USERNAME |
| `EMAIL_TO` | Your email to receive summaries | Your preferred email |

**Important for Gmail Users:**
- You MUST use an [App Password](https://myaccount.google.com/apppasswords), not your regular Gmail password
- Enable 2-Factor Authentication first
- Generate a new app password specifically for "Mail"

### 3. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. If Actions are disabled, enable them
4. You should see 5 workflows:
   - Bloomberg Brief Daily Summary
   - Bloomberg Surveillance Daily Summary
   - Daybreak Europe Daily Summary
   - The China Show Daily Summary
   - The Close Daily Summary

### 4. Test Manually (Optional but Recommended)

Before waiting for the scheduled time, test each workflow manually:

1. Go to **Actions** tab
2. Select a workflow (e.g., "Bloomberg Brief Daily Summary")
3. Click **Run workflow** dropdown
4. Click **Run workflow** button
5. Wait a few minutes and check:
   - The workflow completes successfully (green checkmark)
   - You receive an email with the summary

If it fails:
- Check the workflow logs for errors
- Verify all secrets are set correctly
- Ensure your API keys are valid

### 5. Monitor Automated Runs

After setup, workflows will run automatically at scheduled times:

**Your Daily Email Schedule (CET):**
- 07:45 - The China Show
- 09:45 - Daybreak Europe
- 14:00-15:00 - Bloomberg Surveillance
- 14:30 - Bloomberg Brief
- 22:45 - The Close

You can monitor runs in the **Actions** tab and receive email notifications if workflows fail.

## Managing the Workflows

### Disable a Specific Show

Edit the workflow file (`.github/workflows/SHOW-NAME.yml`) and comment out the schedule:

```yaml
on:
  # schedule:
  #   - cron: '30 13 * * 1-5'
  workflow_dispatch:  # Keep this to allow manual runs
```

Or disable it in [shows_config.yaml](shows_config.yaml):
```yaml
bloomberg_brief:
  enabled: false  # Change to false
```

### Change Schedule Times

Edit the cron expression in the workflow file. Times are in **UTC**:

```yaml
schedule:
  - cron: '30 13 * * 1-5'  # MM HH * * DOW
  #         ^^  ^^      ^^
  #         |   |       |
  #         |   |       Day of week (1-5 = Mon-Fri)
  #         |   Hour (0-23, UTC)
  #         Minute (0-59)
```

**CET to UTC Conversion:**
- CET is UTC+1 (winter)
- CEST is UTC+2 (summer)

Example: To run at 15:00 CET → use `0 14` (14:00 UTC in winter) or `0 13` (13:00 UTC in summer)

### View Logs and Errors

1. Go to **Actions** tab
2. Click on a workflow run
3. Click on the job name
4. Expand steps to see detailed logs

## Repository Permissions

GitHub Actions needs write permissions to commit state files:

1. Go to **Settings** → **Actions** → **General**
2. Scroll to **Workflow permissions**
3. Select **Read and write permissions**
4. Click **Save**

## Cost Estimates

**GitHub Actions:**
- Free tier: 2,000 minutes/month for private repos
- Each run takes ~2-5 minutes
- 5 shows × 5 days × 4 weeks = 100 runs/month = 200-500 minutes
- Well within free tier!

**API Costs (per video):**
- YouTube API: ~1-3 quota units (10,000 free daily)
- Claude API: ~$0.05-$0.15 per video
- **Total: ~$4.50-$13.50/month for 5 daily shows**

## Troubleshooting

### Workflow fails with "No module named 'yaml'"

Add `pyyaml` to [requirements.txt](requirements.txt):
```
pyyaml
```

### Email not sending

- Verify SMTP secrets are correct
- Check that Gmail App Password is used (not regular password)
- Test locally first: `python3 main.py --test-email`

### "Video already processed" error

This is normal - the workflow checks if it already processed today's video. If you want to reprocess:
- Delete the `.last_processed_*` file for that show
- Or run with `--force` flag (edit workflow temporarily)

### Workflow not running at scheduled time

- GitHub Actions may have 5-15 minute delays during high usage
- Check the Actions tab for queued runs
- Weekends: Workflows are set for Mon-Fri only

### Repository not updating

Check workflow permissions (see "Repository Permissions" above).

## Advanced: Combining into Daily Digest

If you prefer one daily email instead of 5 separate emails:

1. Edit [shows_config.yaml](shows_config.yaml):
```yaml
email:
  send_individual: false
  send_daily_digest: true
  digest_time: "18:00"  # 7pm CET
```

2. Create a new workflow `.github/workflows/daily-digest.yml`:
```yaml
name: Daily Digest
on:
  schedule:
    - cron: '0 18 * * 1-5'  # 7pm CET = 6pm UTC (winter)
  workflow_dispatch:
# ... (process all shows and send digest)
```

## Support

If you encounter issues:
1. Check workflow logs in Actions tab
2. Review [SCHEDULING_GUIDE.md](SCHEDULING_GUIDE.md)
3. Test locally first: `python3 process_show.py bloomberg_brief --no-email`

## Next Steps

Once working:
- ✅ Summaries arrive automatically each weekday
- ✅ State files prevent duplicate processing
- ✅ New summaries saved to `summaries/` folder
- ✅ GitHub commits track history

Enjoy your automated Bloomberg intelligence feed!
