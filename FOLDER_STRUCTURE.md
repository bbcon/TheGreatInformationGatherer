# Folder Structure

Your summaries are organized by show name and date for easy browsing.

## Current Structure (by_show)

```
summaries/
├── bloomberg_brief/
│   ├── 2026-01-14/
│   │   ├── summary_4HznktOR_kg_20260114_172008.json
│   │   └── summary_4HznktOR_kg_20260114_172008.md
│   ├── 2026-01-15/
│   │   └── ...
│   └── 2026-01-16/
│       └── ...
├── bloomberg_surveillance/
│   ├── 2026-01-14/
│   └── ...
├── daybreak_europe/
│   ├── 2026-01-14/
│   └── ...
├── the_china_show/
│   ├── 2026-01-14/
│   └── ...
└── the_close/
    ├── 2026-01-14/
    └── ...

transcripts/
└── (same structure as summaries)
```

## Benefits

**Easy Navigation:**
- Browse by show name first
- Then drill down by date
- All summaries from one show in one place

**Clear Organization:**
- Each show has its own folder
- Date-based subfolders keep it chronological
- No mixing of different shows

## File Naming Convention

Files are named with the pattern:
```
summary_{VIDEO_ID}_{TIMESTAMP}.{json|md}
```

Example:
```
summary_4HznktOR_kg_20260114_172008.md
         ^^^^^^^^^^^  ^^^^^^^^  ^^^^^^
         |            |         |
         Video ID     Date      Time
```

## Alternative Structures

You can change the folder structure in [config.yaml](config.yaml):

### Option 1: By Show (current default)
```yaml
output:
  folder_structure: 'by_show'
```
Result: `summaries/bloomberg_brief/2026-01-14/summary_xxx.md`

### Option 2: By Date
```yaml
output:
  folder_structure: 'by_date'
```
Result: `summaries/2026-01-14/summary_xxx.md`
(All shows mixed together by date)

### Option 3: Flat
```yaml
output:
  folder_structure: 'flat'
```
Result: `summaries/summary_xxx.md`
(All files in one folder)

## Finding Summaries

**Browse by show:**
```bash
# List all Bloomberg Brief summaries
ls -lR summaries/bloomberg_brief/

# Find latest Bloomberg Brief
find summaries/bloomberg_brief -name "*.md" | sort | tail -1
```

**Browse by date:**
```bash
# All summaries from today
find summaries -name "2026-01-14" -type d

# All shows from specific date
find summaries/*/2026-01-14/ -name "*.md"
```

**Search content:**
```bash
# Find summaries mentioning "Fed"
grep -r "Fed" summaries/*/2026-01-*/*.md

# Find summaries with specific action items
grep -A5 "Action Items" summaries/bloomberg_brief/*/summary*.md
```

## Cleaning Up Old Summaries

Keep last 30 days:
```bash
find summaries -type d -name "2025-*" -exec rm -rf {} +
```

Keep specific shows only:
```bash
# Remove Daybreak Europe summaries older than 7 days
find summaries/daybreak_europe -type d -mtime +7 -exec rm -rf {} +
```

## GitHub Actions Behavior

When workflows run:
1. Process show
2. Save to `summaries/{show_name}/{date}/`
3. Commit files to repository
4. You can browse on GitHub or clone locally

## Storage Estimates

Per summary:
- Markdown: ~5-15 KB
- JSON: ~10-20 KB
- Total: ~15-35 KB per video

Monthly storage (5 shows × 20 business days):
- ~100 summaries/month
- ~1.5-3.5 MB/month
- Easily manageable in Git

Annual: ~18-42 MB (very reasonable)
