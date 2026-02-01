#!/usr/bin/env python3
"""
Generate a daily macro brief by combining summaries from all Bloomberg shows.
Output is formatted for Substack publication.
"""
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
import anthropic

load_dotenv()

# Shows to aggregate (in order of processing)
SHOWS = [
    'bloomberg_brief',
    'bloomberg_surveillance',
    'daybreak_europe',
    'the_china_show',
    'the_close'
]

OUTPUT_DIR = Path('summaries/_daily_briefs')

SYSTEM_PROMPT = """You are writing a daily macro brief for a professional audience of macro strategists and portfolio managers.

TONE:
- Write like a Goldman Sachs research note, not a news article
- Be measured and analytical - avoid sensationalism
- Use strong words (historic, unprecedented, crisis) ONLY when truly justified - not for routine market moves
- Default to neutral language: fell/rose, declined/gained, increased/decreased
- Let data speak for itself - "gold fell 8%" is impactful without adding "worst since 1983"
- Readers are sophisticated professionals who find unnecessary hyperbole off-putting

MACRO CONSISTENCY:
- Ensure all narratives are logically consistent
- Think through cause and effect: policy X should logically lead to market reaction Y
- If data seems contradictory, note the tension rather than glossing over it

ACKNOWLEDGE UNCERTAINTY:
- Don't over-interpret single days of data
- Use hedging language where appropriate: "appears to," "may signal"
- Distinguish between what happened (facts) and what it means (interpretation)

GUIDELINES:
- Lead with facts, not interpretation
- Use specific numbers and data points
- Provide context where helpful (e.g., "above consensus expectations of X")
- Let readers draw their own conclusions
- Cut through noise - only include developments that genuinely matter
- Do NOT mention Bloomberg, TV shows, or any source attribution
- When shows report conflicting data (e.g., morning show says dollar up, evening show says dollar down), use the LATEST data

WHAT TO INCLUDE:
- Key economic data releases with actual numbers and context
- Central bank statements, policy decisions, and notable quotes
- Significant market moves with levels and percentages
- Corporate news: earnings, guidance, deals
- Geopolitical developments with market relevance

WHAT TO EXCLUDE:
- Pure speculation or predictions without basis
- Minor moves or noise that don't matter
- Repetitive coverage (consolidate)

OUTPUT FORMAT:
- Start with a 1-2 sentence lead summarizing the day's most important development
- Use **bold section headers** to organize content by theme (e.g., **Fed & Monetary Policy**, **Equities & Earnings**, **Commodities**, etc.)
- Within each section, use a MIX of:
  - Short introductory sentence or context (1-2 sentences max)
  - Bullet points for specific data, moves, or facts (use "-" for bullets)
- Target ~750 words (be concise)
- IMPORTANT: Always leave a blank line before starting a bullet list
"""

USER_PROMPT_TEMPLATE = """Here are summaries from market coverage for {date}. Write a comprehensive daily brief covering the key facts and developments.

{summaries}

Generate the daily brief now. Lead with facts, ~750 words. Use bullet points liberally within each section for key data and moves."""


def load_summaries_for_date(date_str: str) -> dict:
    """Load all show summaries for a given date."""
    summaries = {}
    base_dir = Path('summaries')

    for show in SHOWS:
        show_dir = base_dir / show / date_str
        if show_dir.exists():
            # Find the markdown file
            md_files = list(show_dir.glob('*.md'))
            if md_files:
                with open(md_files[0], 'r') as f:
                    content = f.read()
                    # Extract just the summary part (skip metadata header and footer)
                    # Format is: [header] --- [content] --- [footer]
                    if '---' in content:
                        parts = content.split('---')
                        if len(parts) >= 2:
                            # Take the main content (between first and second ---)
                            content = parts[1].strip()
                    summaries[show] = content

    return summaries


def generate_daily_brief(date_str: str, summaries: dict) -> str:
    """Use Claude to generate the daily brief."""
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # Format summaries for the prompt
    summaries_text = ""
    for show, content in summaries.items():
        # Clean show name for display
        show_display = show.replace('_', ' ').title()
        summaries_text += f"\n\n=== Coverage {len(summaries_text.split('==='))} ===\n{content}"

    # Format date nicely
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    date_display = date_obj.strftime('%B %d, %Y')

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2500,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(
                    date=date_display,
                    summaries=summaries_text
                )
            }
        ],
        system=SYSTEM_PROMPT
    )

    return response.content[0].text, response.usage


def save_daily_brief(date_str: str, content: str):
    """Save the daily brief to the output directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Format date for title
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    date_display = date_obj.strftime('%B %d, %Y')

    # Create markdown file
    filename = OUTPUT_DIR / f"{date_str}_daily_brief.md"

    full_content = f"""# {date_display}

{content}
"""

    with open(filename, 'w') as f:
        f.write(full_content)

    print(f"Saved: {filename}")
    return filename


def get_available_dates() -> list:
    """Get all dates that have at least one show summary."""
    dates = set()
    base_dir = Path('summaries')

    for show in SHOWS:
        show_dir = base_dir / show
        if show_dir.exists():
            for date_dir in show_dir.iterdir():
                if date_dir.is_dir() and date_dir.name.startswith('2026-'):
                    dates.add(date_dir.name)

    return sorted(dates)


def main():
    parser = argparse.ArgumentParser(
        description='Generate daily macro brief from show summaries'
    )
    parser.add_argument(
        '--date',
        type=str,
        help='Date to generate brief for (YYYY-MM-DD). Default: latest available.'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate briefs for all available dates'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing briefs'
    )

    args = parser.parse_args()

    available_dates = get_available_dates()

    if not available_dates:
        print("No summaries found.")
        sys.exit(1)

    if args.all:
        dates_to_process = available_dates
    elif args.date:
        if args.date not in available_dates:
            print(f"No summaries found for {args.date}")
            print(f"Available dates: {', '.join(available_dates[-5:])}")
            sys.exit(1)
        dates_to_process = [args.date]
    else:
        # Default to latest
        dates_to_process = [available_dates[-1]]

    total_cost = 0

    for date_str in dates_to_process:
        output_file = OUTPUT_DIR / f"{date_str}_daily_brief.md"

        if output_file.exists() and not args.force:
            print(f"Skipping {date_str} (already exists, use --force to overwrite)")
            continue

        print(f"\n{'='*60}")
        print(f"Generating daily brief for {date_str}")
        print(f"{'='*60}")

        # Load summaries
        summaries = load_summaries_for_date(date_str)

        if not summaries:
            print(f"No summaries found for {date_str}, skipping.")
            continue

        print(f"Found {len(summaries)} show summaries: {', '.join(summaries.keys())}")

        # Generate brief
        try:
            content, usage = generate_daily_brief(date_str, summaries)
            cost = (usage.input_tokens * 0.003 / 1000 + usage.output_tokens * 0.015 / 1000)
            total_cost += cost
            print(f"Generated ({usage.input_tokens} in, {usage.output_tokens} out, ${cost:.4f})")

            # Save
            save_daily_brief(date_str, content)

        except Exception as e:
            print(f"Error generating brief for {date_str}: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"Done! Total cost: ${total_cost:.4f}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
