# Gmail App Password Setup Guide

## Why You Need This

Gmail requires **App Passwords** for third-party apps (like this script). It's more secure than using your regular password.

## Step-by-Step Setup (5 minutes)

### Step 1: Enable 2-Factor Authentication

1. Go to: https://myaccount.google.com/security
2. Scroll to "How you sign in to Google"
3. Click **"2-Step Verification"**
4. Click **"Get Started"**
5. Follow the prompts to set up 2FA (use phone number or authenticator app)

**Note:** You MUST have 2FA enabled to create App Passwords

### Step 2: Create App Password

1. Go to: https://myaccount.google.com/apppasswords
2. You may need to sign in again
3. Under "Select app", choose **"Mail"**
4. Under "Select device", choose **"Other (Custom name)"**
5. Type: **"Newsletter Summarizer"**
6. Click **"Generate"**
7. **COPY THE 16-CHARACTER PASSWORD** (looks like: `xxxx xxxx xxxx xxxx`)
   - You'll only see this once!
   - Paste it immediately into your .env file

### Step 3: Enable IMAP in Gmail

1. Go to: https://mail.google.com/mail/u/0/#settings/fwdandpop
2. Click **"Forwarding and POP/IMAP"** tab
3. Under "IMAP access", select **"Enable IMAP"**
4. Click **"Save Changes"**

### Step 4: Add to .env File

```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx  # The 16-char password from Step 2
```

**Important:** Use the App Password, NOT your regular Gmail password!

## Verification Test

Test your setup:

```bash
python3 -c "
import imaplib
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('YOUR_EMAIL', 'YOUR_APP_PASSWORD')
print('✅ Gmail connection works!')
"
```

## Troubleshooting

### "Invalid credentials" error
- ✓ Make sure you're using the **App Password**, not your regular password
- ✓ Check for extra spaces in the password
- ✓ App Password should be 16 characters (with or without spaces)
- ✓ Try generating a new App Password

### "Can't find App Passwords option"
- ✓ Make sure 2-Factor Authentication is enabled first
- ✓ Try this direct link: https://myaccount.google.com/apppasswords
- ✓ If still not there, your account type might not support it (some business accounts)

### "IMAP access disabled"
- ✓ Enable IMAP in Gmail settings: https://mail.google.com/mail/u/0/#settings/fwdandpop
- ✓ Wait 5 minutes after enabling, then try again

### Still having issues?
Try the Google Account troubleshooter: https://support.google.com/accounts/answer/185833

## Security Tips

✅ **Good practices:**
- App Password is specific to this script only
- Can revoke at any time without affecting your main account
- More secure than your regular password
- Can create multiple App Passwords for different apps

❌ **Never:**
- Share your App Password publicly
- Use your regular Gmail password in scripts
- Commit .env file to Git (it's in .gitignore)

## Alternative: OAuth2

For even more security, you can use OAuth2 instead of App Passwords. This requires more setup but doesn't require storing passwords.

See: https://developers.google.com/gmail/api/auth/web-server

## Quick Reference

- **Enable 2FA:** https://myaccount.google.com/security
- **Create App Password:** https://myaccount.google.com/apppasswords
- **Enable IMAP:** https://mail.google.com/mail/u/0/#settings/fwdandpop
- **Help:** https://support.google.com/accounts/answer/185833

---

Once you have your App Password, you're ready to run the newsletter summarizer! 🚀
