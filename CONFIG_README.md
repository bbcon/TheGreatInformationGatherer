# Configuration Guide

The Great Information Gatherer can be customized via `config.yaml` to control summary style, length, and output format.

## Quick Start

Edit `config.yaml` to customize your summaries:

```bash
nano config.yaml
```

## Configuration Options

### Summary Length

Control how detailed the summary is:

```yaml
summary:
  length: 'standard'  # Options: 'concise', 'standard', 'detailed'
```

- **concise**: Very brief, 1-2 sentences per section
- **standard**: Balanced with key details (recommended)
- **detailed**: Comprehensive analysis with full context

### Summary Sections

Enable/disable specific sections:

```yaml
summary:
  sections:
    executive_summary: true        # High-level overview
    macro_indicators: true         # Economic data points
    market_outlook: true           # Asset class views
    central_bank_policy: true      # Fed, ECB, BOJ updates
    risks_catalysts: true          # Key risks to watch
    technical_levels: false        # Chart levels (if discussed)
    actionable_takeaways: true     # Trading insights
```

Set any section to `false` to exclude it from summaries.

### Summary Style

```yaml
summary:
  style:
    tone: 'analytical'              # Options: 'analytical', 'concise', 'detailed'
    angle: 'macro_trading'          # Focus: 'macro_trading', 'risk_management', 'fundamental_analysis'
    include_data_points: true       # Emphasize numbers and data
    emphasize_actionable: true      # Focus on tradeable insights
```

### Custom Instructions

Add your own custom requirements:

```yaml
custom_instructions: |
  Focus on implications for global macro trading strategies.
  Highlight any divergences from consensus views.
  Note any unusual market behavior or outlier data points.
  Pay special attention to currency and rates markets.
```

### Output Settings

Control file formats and folder structure:

```yaml
output:
  save_json: true           # Save JSON format
  save_markdown: true       # Save Markdown format (.md)

  # Folder structure options
  folder_structure: 'by_date'  # Options: 'by_date' or 'flat'
  date_format: 'YYYY-MM-DD'    # Used when folder_structure is 'by_date'
```

**by_date structure:**
```
summaries/
  2026-01-13/
    MF3ywfAWVuE_20260113_172925.md
    MF3ywfAWVuE_20260113_172925.json
  2026-01-12/
    emOSv5hRPOI_20260112_151520.md
    emOSv5hRPOI_20260112_151520.json
```

**flat structure:**
```
summaries/
  MF3ywfAWVuE_20260113_172925.md
  MF3ywfAWVuE_20260113_172925.json
  emOSv5hRPOI_20260112_151520.md
  emOSv5hRPOI_20260112_151520.json
```

### Email Settings

Configure which sections appear in emails:

```yaml
email:
  # Only include these sections in email (to keep emails shorter)
  include_sections:
    - executive_summary
    - macro_indicators
    - market_outlook
    - actionable_takeaways

  format: 'html'  # Options: 'html' or 'plain'
  include_file_link: true  # Link to full summary file
```

## Example Configurations

### For Quick Daily Briefings

```yaml
summary:
  length: 'concise'
  sections:
    executive_summary: true
    macro_indicators: true
    market_outlook: true
    central_bank_policy: false
    risks_catalysts: false
    technical_levels: false
    actionable_takeaways: true
```

### For Deep Analysis

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
  style:
    include_data_points: true
    emphasize_actionable: true
```

### For Risk Management Focus

```yaml
summary:
  style:
    angle: 'risk_management'
  sections:
    executive_summary: true
    macro_indicators: true
    central_bank_policy: true
    risks_catalysts: true
    actionable_takeaways: true
    # Disable market outlook and technical
    market_outlook: false
    technical_levels: false

custom_instructions: |
  Focus on downside risks and tail scenarios.
  Highlight divergences and potential market stress signals.
  Emphasize risk/reward asymmetries.
```

## Testing Your Configuration

Test your config changes without sending email:

```bash
python3 main.py --video-id VIDEO_ID --no-email
```

Then check the output in `summaries/YYYY-MM-DD/` folder.

## Notes

- Changes take effect immediately (no restart needed)
- The tool falls back to defaults if config is invalid
- Markdown files (.md) are perfect for viewing in editors or committing to git
- JSON files contain full metadata and are better for programmatic access
