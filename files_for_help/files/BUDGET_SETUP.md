# 💰 Budget Setup Guide - FREE or Low-Cost Options

## Total Cost Comparison

### 🎉 **FREE Option** (Recommended for personal use)
- **Transcription:** FREE (YouTube auto-captions)
- **Summarization:** Pay-as-you-go (~$0.10-0.30/day)
- **Total:** ~$3-9/month

### 💸 **Premium Option**
- **Transcription:** OpenAI Whisper API (~$0.30-0.60/video)
- **Summarization:** Claude/GPT (~$0.10-0.30/day)
- **Total:** ~$12-27/month

---

## 🆓 FREE Transcription Setup (Recommended!)

Bloomberg videos on YouTube have **auto-generated captions** that are FREE to extract!

### How It Works
1. yt-dlp downloads YouTube's auto-captions (no video download needed)
2. Extracts text from caption files
3. Zero API costs!

### Setup
Already configured by default in `config.yaml`:

```yaml
transcription:
  use_free_youtube_captions: true  # ✅ Already set to true!
```

**No API key needed for transcription!** 🎉

### Accuracy
- YouTube auto-captions are 70-80% accurate
- Good enough for Bloomberg content (clear audio, professional speakers)
- You're summarizing anyway, so minor errors don't matter much

---

## 💡 Low-Cost Summarization

You **only** need ONE API key for summarization:

### Option 1: Anthropic Claude (Recommended)
**Best for:** High-quality financial analysis

**Pricing:**
- Claude Sonnet: ~$0.003 per 1K tokens
- Average summary: ~$0.10-0.30 each
- **Monthly cost:** ~$3-9 for daily summaries

**Setup:**
```bash
# Get free API key with $5 credit
# Sign up: https://console.anthropic.com

# In .env file:
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

### Option 2: OpenAI GPT (Alternative)
**Pricing:**
- GPT-4 Turbo: ~$0.01 per 1K tokens  
- Average summary: ~$0.15-0.40 each
- **Monthly cost:** ~$4.50-12 for daily summaries

**Setup:**
```bash
# Sign up: https://platform.openai.com

# In .env file:
OPENAI_API_KEY=sk-xxxxx
```

---

## 🎯 Recommended Budget Setup

### For $3-9/month:

1. **Use FREE YouTube captions** (already configured!)
   ```yaml
   transcription:
     use_free_youtube_captions: true
   ```

2. **Use Anthropic Claude** for summaries
   ```yaml
   summary:
     provider: "anthropic"
     model: "claude-sonnet-4-20250514"
   ```

3. **Set ONLY this in .env:**
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
   ```

**That's it!** Total cost: ~$0.10-0.30 per day = **$3-9/month**

---

## 🔍 Cost Breakdown

### What You're Actually Paying For:

**FREE:**
- ✅ Video downloading (yt-dlp)
- ✅ Transcript extraction (YouTube captions)
- ✅ All the Python code and automation

**PAID (~$0.10-0.30/day):**
- ❌ AI Summarization (Claude/GPT)
  - This is the ONLY cost
  - Worth it for 5-10 minutes of analysis work saved daily

---

## 💳 API Key Setup (Just Anthropic)

### Step 1: Get Anthropic API Key (5 minutes)

1. Go to https://console.anthropic.com
2. Sign up (email + password)
3. Verify email
4. Go to "API Keys" section
5. Click "Create Key"
6. Copy the key (starts with `sk-ant-api03-`)

### Step 2: Add to .env File

```bash
cd bloomberg-markets-summarizer
nano .env
```

Add this line:
```
ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE
```

Save and exit (Ctrl+X, Y, Enter)

**Done!** 🎉

---

## 📊 Cost Examples

### Daily Costs:
- **Monday:** $0.25 (longer video)
- **Tuesday:** $0.15 (shorter video)  
- **Wednesday:** $0.20 (average video)
- **Thursday:** $0.18 (average video)
- **Friday:** $0.22 (average video)

**Weekly:** ~$1.00  
**Monthly:** ~$4.00

### Compare to Alternatives:
- **Bloomberg Terminal:** $2,000+/month 🤯
- **Professional research service:** $50-500/month
- **Your time manually watching:** 20 hours/month = priceless

**This solution:** $4/month ✨

---

## 🚀 Quick Start (Free Version)

```bash
# 1. Install (one time)
./install.sh

# 2. Add ONLY Anthropic API key
echo "ANTHROPIC_API_KEY=sk-ant-api03-xxxxx" > .env

# 3. Run (FREE transcript + cheap AI summary)
python3 main.py
```

**That's it!** No OpenAI key needed, no paid transcription, just one API key!

---

## ⚙️ Advanced: Even Cheaper Options

### Option A: Free AI Summarization (Experimental)
Use local LLMs like Llama or Mistral (free but requires GPU):
- Ollama (free, local)
- LM Studio (free, local)
- Requires: 8GB+ RAM, decent GPU

### Option B: Reduce Summary Length
In `config.yaml`:
```yaml
summary:
  detail_level: "brief"  # Shorter = cheaper
  max_tokens: 1000  # Reduce from 2000
```
**Savings:** ~50% cost reduction

### Option C: Summary Every Other Day
Run cron every 2 days instead of daily:
```bash
# In crontab -e:
0 7 */2 * * cd /path/to/repo && python3 main.py
```
**Savings:** 50% cost reduction

---

## ❓ FAQ

**Q: Do I really only need one API key?**  
A: Yes! Just Anthropic Claude. YouTube captions are FREE.

**Q: What if YouTube video doesn't have captions?**  
A: Very rare for Bloomberg. If it happens, you'd need paid transcription for that video.

**Q: Can I use a free AI for summaries too?**  
A: Yes, but quality drops significantly. Claude Sonnet is worth the $0.20/day.

**Q: How much is the first month?**  
A: ~$3-9. Anthropic gives you $5 free credit to start!

**Q: Can I cancel anytime?**  
A: Yes! It's pay-as-you-go. No subscription.

---

## 🎁 Free Trial

Anthropic gives **$5 free credit** when you sign up!

That's enough for:
- **25-50 summaries**
- **Nearly 2 months** of free use
- Test the system risk-free

After free credit, it's only $3-9/month.

---

## 📈 Value Proposition

**What you get:**
- Daily professional market summaries
- Key insights extracted automatically
- Saves 30+ minutes daily
- Delivered to your inbox (optional)

**What you pay:**
- ~$0.10-0.30 per day
- ~$3-9 per month
- Less than one coffee ☕

**ROI:** If your time is worth >$2/hour, this pays for itself instantly.

---

## 🔒 Privacy & Security

- API keys stored locally in `.env` (never uploaded)
- No data stored by Bloomberg or YouTube
- Transcripts and summaries stored locally
- You own all the data

---

## ✅ Ready to Start?

```bash
# Get the repo (you already have it!)
cd bloomberg-markets-summarizer

# Install dependencies
./install.sh

# Get Anthropic API key (5 minutes)
# Visit: https://console.anthropic.com

# Add to .env
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# Run it!
python3 main.py

# Cost: ~$0.20 for this one summary
```

**Welcome to affordable, automated market intelligence!** 🚀
