# Configuration Guide

The `config.yaml` file allows you to customize how summaries are generated, formatted, and delivered.

## Summary Settings

### Length Options

```yaml
summary:
  length: 'concise'  # Options: 'concise', 'standard', 'detailed'
```

- **concise**: Brief summaries, 1-2 sentences per section (fastest, cheapest ~1000 tokens)
- **standard**: Balanced detail (default, ~1500-2000 tokens)
- **detailed**: Comprehensive analysis with extensive detail (~2500+ tokens)

### Sections

Enable or disable specific sections in your summary:

```yaml
summary:
  sections:
    executive_summary: true      # 2-3 sentence overview
    macro_indicators: true        # Economic data, GDP, inflation, etc.
    market_outlook: true          # Asset class views, positioning
    central_bank_policy: true     # Fed, ECB, BOJ commentary
    risks_catalysts: true         # Risks and upcoming events
    technical_levels: false       # Chart levels (set to true if needed)
    actionable_takeaways: true    # Key action items
```

**Tip**: Disable sections you don't need to make summaries shorter and reduce costs.

### Custom Instructions

Add your own instructions to guide the AI:

```yaml
custom_instructions: |
  Focus on implications for global macro trading strategies.
  Highlight any divergences from consensus views.
  Note any unusual market behavior or outlier data points.
  Prioritize Fed policy and DXY movements.
```

## Output Settings

### File Formats

```yaml
output:
  save_json: true       # Structured data format
  save_markdown: true   # Human-readable format
```

Both formats are saved automatically. The markdown file is perfect for reading, while JSON is useful for programmatic access.

### Folder Structure

```yaml
output:
  folder_structure: 'by_date'  # Options: 'flat' or 'by_date'
  date_format: 'YYYY-MM-DD'     # Or 'YYYY/MM'
```

- **by_date**: Organizes summaries into date folders
  - Example: `summaries/2026-01-13/summary_VIDEO_ID.md`
  - Keeps things organized long-term

- **flat**: All summaries in one folder
  - Example: `summaries/summary_VIDEO_ID_20260113.md`
  - Simpler but harder to manage over time

## Email Settings

### Sections to Include

```yaml
email:
  include_sections:
    - executive_summary
    - actionable_takeaways
```

**Tip**: Email summaries can be shorter than saved summaries. Only include sections you want in your inbox. The full summary is always saved to disk.

### Email Format

```yaml
email:
  format: 'html'  # Options: 'html' or 'plain'
```

- **html**: Properly formatted with bold, headers, lists (recommended)
- **plain**: Plain text fallback

## Example Configurations

### Minimal Setup (Fast & Cheap)

For quick daily briefings:

```yaml
summary:
  length: 'concise'
  sections:
    executive_summary: true
    actionable_takeaways: true
    macro_indicators: false
    market_outlook: false
    central_bank_policy: false
    risks_catalysts: false
    technical_levels: false

output:
  save_markdown: true
  save_json: false
  folder_structure: 'flat'

custom_instructions: |
  Maximum brevity. Only the most critical information.
```

**Cost**: ~$0.02-0.03 per video
**Length**: 200-400 words

### Comprehensive Analysis

For detailed research:

```yaml
summary:
  length: 'detailed'
  sections:
    executive_summary: true
    macro_indicators: true
    market_outlook: true
    central_bank_policy: true
    risks_catalysts: true
    technical_levels: true
    actionable_takeaways: true

custom_instructions: |
  Provide extensive analysis with all relevant details.
  Include specific data points, dates, and numbers.
  Analyze second-order effects and market implications.
```

**Cost**: ~$0.10-0.15 per video
**Length**: 1500-2500 words

### Fed-Focused Configuration

For central bank watchers:

```yaml
summary:
  length: 'standard'
  sections:
    executive_summary: true
    macro_indicators: true
    market_outlook: false
    central_bank_policy: true  # FOCUS
    risks_catalysts: true
    technical_levels: false
    actionable_takeaways: true

custom_instructions: |
  Prioritize Federal Reserve commentary and policy implications.
  Focus on rate expectations, dot plot changes, and forward guidance.
  Highlight any shifts in Fed rhetoric or stance.
```

## Editing the Config

1. Open `config.yaml` in any text editor
2. Make your changes
3. Save the file
4. Run the script - changes take effect immediately

No need to restart or reinstall anything!

## Testing Your Config

```bash
# Test with a specific video
python3 main.py --video-id VIDEO_ID --no-email

# Check the output
cat summaries/2026-01-13/summary_VIDEO_ID*.md
```

## Tips & Best Practices

1. **Start with 'concise'** - You can always increase detail later
2. **Disable unused sections** - Saves tokens and money
3. **Customize instructions** - Tell the AI exactly what you want
4. **Use date folders** - Keeps things organized long-term
5. **Test incrementally** - Change one thing at a time

## Troubleshooting

### Summary is too long

- Change `length` to `'concise'`
- Disable sections you don't need
- Add instruction: "Maximum brevity. Use bullet points."

### Summary lacks detail

- Change `length` to `'detailed'`
- Add custom instructions for specific focus areas
- Enable more sections

### Missing information

- Enable relevant sections
- Add custom instructions like: "Always include specific numbers and data points"

### Email not rendering properly

- Ensure `format: 'html'` is set
- Check your email client supports HTML (most do)
- The markdown to HTML converter now properly handles **bold**, *italic*, and lists

## Cost Management

Summary costs scale with length:

- **concise**: ~500-1000 output tokens = $0.02-0.03
- **standard**: ~1500-2000 output tokens = $0.05-0.07
- **detailed**: ~2500-3500 output tokens = $0.08-0.12

Input tokens (transcript) are ~10,000 tokens = $0.01-0.02

**Daily cost at 1 video/day:**
- Concise: ~$1/month
- Standard: ~$2/month
- Detailed: ~$3.50/month

## Advanced: Section-Specific Instructions

You can add instructions for specific sections in your custom_instructions:

```yaml
custom_instructions: |
  Executive Summary: Focus on the single most important takeaway.
  Macro Indicators: Always include actual numbers and % changes.
  Market Outlook: Prioritize FX and rates over equities.
  Actionable Takeaways: Maximum 3 items, very specific.
```

## Need Help?

- Check [README.md](README.md) for full documentation
- See [QUICKSTART.md](QUICKSTART.md) for setup guide
- Review example configurations above
