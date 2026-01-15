# Quick Reference

## Running the Tool

```bash
# Automatic (fetches latest video)
python3 main.py

# Specific video, no email
python3 main.py --video-id VIDEO_ID --no-email

# Force reprocess
python3 main.py --force

# Test email config
python3 main.py --test-email
```

## Output Locations

```
summaries/2026-01-13/
├── summary_VIDEO_ID.md    ← Read this!
└── summary_VIDEO_ID.json  ← Data format

transcripts/2026-01-13/
└── transcript_VIDEO_ID.json
```

## Quick Customization

Edit `config.yaml`:

### Make Summaries Shorter
```yaml
summary:
  length: 'concise'  # Was 'standard'
```

### Disable Sections
```yaml
summary:
  sections:
    technical_levels: false
    risks_catalysts: false
```

### Add Focus
```yaml
custom_instructions: |
  Focus on Fed policy.
  Prioritize DXY and rates.
```

## Common Tasks

### Change Summary Length
```yaml
# In config.yaml
summary:
  length: 'concise'   # Short (~200 words, ~$0.02)
  # length: 'standard'  # Medium (~500 words, ~$0.07)
  # length: 'detailed'  # Long (~2000 words, ~$0.12)
```

### Use Flat Folder Structure
```yaml
# In config.yaml
output:
  folder_structure: 'flat'  # All files in summaries/
```

### Customize Email
```yaml
# In config.yaml
email:
  include_sections:
    - executive_summary  # Only these in email
    - actionable_takeaways
```

## File Structure

```
.
├── config.yaml          ← YOUR settings
├── .env                 ← API keys
├── main.py              ← Run this
├── summaries/           ← Output here
│   └── 2026-01-13/
│       └── *.md        ← Read these
└── transcripts/         ← Raw transcripts
```

## Cost Control

| Setting | Cost/video |
|---------|------------|
| length: concise | $0.02 |
| length: standard | $0.07 |
| length: detailed | $0.12 |

Tips:
- Use 'concise' for daily briefings
- Disable unused sections
- Costs = input (~$0.01) + output (varies)

## Getting Help

- [IMPROVEMENTS.md](IMPROVEMENTS.md) - What's new
- [CONFIG_GUIDE.md](CONFIG_GUIDE.md) - Full config docs
- [README.md](README.md) - Complete guide
- [QUICKSTART.md](QUICKSTART.md) - Setup guide

## Most Common Edits

```yaml
# In config.yaml

# 1. Make it shorter
summary:
  length: 'concise'

# 2. Fewer sections
summary:
  sections:
    executive_summary: true
    actionable_takeaways: true
    macro_indicators: false
    market_outlook: false
    central_bank_policy: false
    risks_catalysts: false

# 3. Custom focus
custom_instructions: |
  Maximum brevity.
  Focus on Fed and rates.
  Only actionable insights.
```

## Quick Fixes

### Too long?
→ Set `length: 'concise'` in config.yaml

### Missing info?
→ Set `length: 'detailed'` in config.yaml

### Don't need a section?
→ Set that section to `false` in config.yaml

### Email not bold?
→ Already fixed! **Bold** now renders properly

### Want flat folders?
→ Set `folder_structure: 'flat'` in config.yaml

## Daily Workflow

1. **Morning**: Run the tool
   ```bash
   python3 main.py
   ```

2. **Read**: Check your email or:
   ```bash
   cat summaries/$(date +%Y-%m-%d)/summary_*.md
   ```

3. **Adjust** (if needed): Edit `config.yaml`

4. **Done!** Summary saved and emailed

## That's It!

Everything is in `config.yaml` - no code changes needed.
