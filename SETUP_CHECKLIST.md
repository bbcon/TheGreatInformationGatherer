# Setup Checklist

Complete these steps to get your automated Bloomberg summaries running.

## ✅ Pre-Setup (Already Done)

- [x] Python dependencies installed
- [x] YouTube API key added to `.env`
- [x] Anthropic API key configured
- [x] 5 Bloomberg shows configured
- [x] GitHub Actions workflows created
- [x] New concise summary format implemented

## 📋 GitHub Setup (Do This Now)

### Step 1: Push to GitHub

```bash
cd /Users/brendanberthold/Dropbox/My\ Computer/GitHub/TheGreatInformationGatherer

# Check status
git status

# Add all files
git add .

# Commit
git commit -m "Add automated multi-show Bloomberg summarizer with GitHub Actions"

# Create repo on GitHub if not exists, then:
# git remote add origin https://github.com/YOUR_USERNAME/TheGreatInformationGatherer.git

# Push
git push -u origin main
```

### Step 2: Add GitHub Secrets

Go to: `https://github.com/YOUR_USERNAME/TheGreatInformationGatherer/settings/secrets/actions`

Add these 8 secrets (click "New repository secret" for each):

| Secret Name | Get From | Notes |
|------------|----------|-------|
| `YOUTUBE_API_KEY` | Your `.env` file | Already configured |
| `ANTHROPIC_API_KEY` | Your `.env` file | Already configured |
| `SMTP_SERVER` | Email provider | Gmail: `smtp.gmail.com` |
| `SMTP_PORT` | Email provider | Gmail: `587` |
| `SMTP_USERNAME` | Your email | The email sending from |
| `SMTP_PASSWORD` | Email app password | [Create here](https://myaccount.google.com/apppasswords) |
| `EMAIL_FROM` | Your email | Same as SMTP_USERNAME |
| `EMAIL_TO` | Your email | Where to receive summaries |

**Gmail App Password:**
1. Enable 2FA on Google account
2. Go to https://myaccount.google.com/apppasswords
3. Create app password for "Mail"
4. Use this 16-character password as `SMTP_PASSWORD`

### Step 3: Enable Workflow Permissions

Go to: `https://github.com/YOUR_USERNAME/TheGreatInformationGatherer/settings/actions`

1. Scroll to "Workflow permissions"
2. Select "Read and write permissions"
3. Click "Save"

### Step 4: Test Workflows Manually

1. Go to Actions tab: `https://github.com/YOUR_USERNAME/TheGreatInformationGatherer/actions`
2. Click "Bloomberg Brief Daily Summary"
3. Click "Run workflow" → "Run workflow"
4. Wait 2-5 minutes
5. Check for:
   - ✅ Green checkmark (success)
   - 📧 Email in your inbox with summary

Repeat for other shows if desired.

## 🎯 Verification

After setup, you should have:

- [ ] Repository pushed to GitHub
- [ ] All 8 secrets added
- [ ] Workflow permissions enabled
- [ ] At least one workflow tested successfully
- [ ] Received test email with summary

## 📅 Schedule Reference (CET)

Your emails will arrive at:

- **07:45** - The China Show
- **09:45** - Daybreak Europe
- **14:00-15:00** - Bloomberg Surveillance
- **14:30** - Bloomberg Brief
- **22:45** - The Close

All Monday-Friday only.

## 🔧 Troubleshooting

**No email received:**
- Check spam folder
- Verify SMTP secrets are correct
- Test locally: `python3 main.py --test-email`

**Workflow fails:**
- Click on failed workflow → View logs
- Common issues:
  - Missing secret
  - Wrong Gmail password (use App Password!)
  - Permissions not enabled

**Video already processed:**
- This is normal after first run
- Each video only processed once per day
- State tracked in `.last_processed_*` files

## 📚 Documentation

- [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - Detailed setup guide
- [SCHEDULE_SUMMARY.md](SCHEDULE_SUMMARY.md) - Quick schedule reference
- [SCHEDULING_GUIDE.md](SCHEDULING_GUIDE.md) - Full scheduling documentation

## 🎉 You're Done!

Once complete, you'll receive 5 automated emails each weekday with concise, scannable Bloomberg show summaries.

Cost: ~$5-14/month for Claude API (everything else is free!)
