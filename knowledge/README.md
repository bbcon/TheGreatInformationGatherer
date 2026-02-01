# Knowledge Base

This folder contains summaries of content that builds **stock knowledge** - foundational understanding of macro, markets, geopolitics, and related topics. Unlike the `summaries/` folder which tracks **daily market updates** (staying current), this folder captures **timeless or structural insights**.

## Folder Structure

```
knowledge/
├── lectures/          # Academic lectures, conference talks, seminars
├── papers/            # Academic papers, research reports
├── books/             # Book summaries and notes
├── podcasts/          # Podcast episode summaries
└── README.md
```

## Naming Convention

Files follow this pattern:
```
YYYY-MM-DD_speaker-or-author_title-slug.md
```

Examples:
- `2026-01-16_adam-tooze_electrostates-petrostates-new-cold-war.md`
- `2025-03-15_ray-dalio_changing-world-order.md`
- `2024-11-20_bridgewater_debt-cycles-research.md`

## Content Structure

Each summary should include:

1. **Metadata header**: Speaker/author, source, date, URL, duration, tags
2. **Core thesis**: Main argument in 2-3 paragraphs
3. **Key concepts**: Definitions and frameworks introduced
4. **Detailed analysis**: Deep dive into major themes
5. **Implications**: For macro-finance analysis, markets, investment
6. **Key quotes**: Memorable passages worth remembering
7. **Generation info**: Tokens used, cost

## Tags

Use consistent tags for cross-referencing:
- Topics: `#energy-transition`, `#china`, `#geopolitics`, `#monetary-policy`, `#fiscal-policy`
- Asset classes: `#equities`, `#fixed-income`, `#fx`, `#commodities`
- Regions: `#us`, `#europe`, `#asia`, `#em`
- Frameworks: `#macro`, `#industrial-policy`, `#climate`

## How to Add Content

To summarize a YouTube video or other content:

```bash
# Request summary in Claude Code conversation
# "Summarize this video: https://youtube.com/watch?v=..."
# Specify if academic lecture, podcast, etc.
```

The summary will be saved to the appropriate subfolder.

## Relationship to Other Folders

- **summaries/**: Daily Bloomberg show summaries (staying current)
- **summaries/_aggregates/**: Weekly/periodic aggregations of daily summaries
- **knowledge/**: Foundational content (building stock knowledge)

Both feed into the book project at `../MacroMarketsBook/`.
