#!/usr/bin/env python3
"""
Generate a weekly macro brief by combining daily briefs.
Highlights key themes and developments across the week.
"""
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
import anthropic

load_dotenv()

DAILY_BRIEFS_DIR = Path('summaries/_daily_briefs')
OUTPUT_DIR = Path('summaries/_weekly_briefs')

SYSTEM_PROMPT = """You are writing a weekly macro brief for a professional audience of macro strategists and portfolio managers.

TONE:
- Write like a Goldman Sachs research note, not a news article
- Be measured and analytical - avoid sensationalism
- Use strong words (historic, unprecedented, crisis) ONLY when truly justified - not for routine market moves
- Default to neutral language: fell/rose, declined/gained, increased/decreased
- Let data speak for itself - the numbers ARE the story
- Readers are sophisticated professionals who find unnecessary hyperbole off-putting

MACRO CONSISTENCY:
- Ensure all narratives are logically consistent
- Example: If "Fed independence under threat" means pressure for LOWER rates (dovish), then nominating a hawkish chair contradicts that narrative - acknowledge the tension
- Think through cause and effect: policy X should logically lead to market reaction Y
- Don't combine contradictory narratives - either reconcile them or note the apparent contradiction

ACKNOWLEDGE UNCERTAINTY:
- Reality is messy - avoid false narrative closure
- Don't declare crises "resolved" when outcomes remain uncertain
- Use hedging language where appropriate: "appears to," "may signal," "remains to be seen"
- Distinguish between what happened (facts) and what it means (interpretation)

GUIDELINES:
- Identify 3-5 key themes that defined the week
- Track how stories evolved across the week
- Use specific numbers and data points
- Note any significant reversals or surprises
- Let readers draw their own conclusions - report facts, not opinions
- Do NOT mention Bloomberg, TV shows, or any source attribution

STRUCTURE:
- Start with a 2-3 sentence lead summarizing the week's key developments
- Use **bold section headers** for each major theme (3-5 themes)
- Within each theme section, use a MIX of:
  - Short introductory context (1-2 sentences)
  - Bullet points for specific data, moves, or developments (use "-" for bullets)
  - Track how the story evolved across different days
- Include a brief "Week Ahead" section with bullet points for key upcoming events
- Target ~1000 words (be concise)
- IMPORTANT: Always leave a blank line before starting a bullet list

WHAT MAKES A GOOD THEME:
- Recurring topics across multiple days
- Major market moves with clear catalysts
- Policy shifts or central bank developments
- Geopolitical events with market implications
- Corporate earnings patterns or sector trends
"""

USER_PROMPT_TEMPLATE = """Here are the daily macro briefs for the week of {week_label}. Synthesize these into a weekly brief that identifies the key themes and tracks how the week's narrative evolved.

{daily_briefs}

Generate the weekly brief now. Identify 3-5 major themes, ~1000 words. Use bullet points liberally within each section for key data and developments."""


def get_week_dates(year: int, week_num: int) -> tuple:
    """Get the start and end dates for a given ISO week."""
    # ISO week starts on Monday
    jan1 = datetime(year, 1, 1)
    # Find the first Monday of week 1
    if jan1.isoweekday() <= 4:
        # Jan 1 is Mon-Thu, it's in week 1
        week1_start = jan1 - timedelta(days=jan1.isoweekday() - 1)
    else:
        # Jan 1 is Fri-Sun, week 1 starts next Monday
        week1_start = jan1 + timedelta(days=8 - jan1.isoweekday())

    week_start = week1_start + timedelta(weeks=week_num - 1)
    week_end = week_start + timedelta(days=6)

    return week_start, week_end


def load_daily_briefs_for_week(year: int, week_num: int) -> dict:
    """Load all daily briefs for a given week."""
    week_start, week_end = get_week_dates(year, week_num)

    briefs = {}
    current = week_start

    while current <= week_end:
        date_str = current.strftime('%Y-%m-%d')
        brief_file = DAILY_BRIEFS_DIR / f"{date_str}_daily_brief.md"

        if brief_file.exists():
            with open(brief_file, 'r') as f:
                content = f.read()
                # Remove the date header line
                lines = content.split('\n')
                if lines and lines[0].startswith('# '):
                    content = '\n'.join(lines[1:]).strip()
                briefs[date_str] = content

        current += timedelta(days=1)

    return briefs


def generate_weekly_brief(year: int, week_num: int, briefs: dict) -> str:
    """Use Claude to generate the weekly brief."""
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    week_start, week_end = get_week_dates(year, week_num)
    week_label = f"{week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}"

    # Format daily briefs
    briefs_text = ""
    for date_str in sorted(briefs.keys()):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_name = date_obj.strftime('%A, %B %d')
        briefs_text += f"\n\n=== {day_name} ===\n{briefs[date_str]}"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(
                    week_label=week_label,
                    daily_briefs=briefs_text
                )
            }
        ],
        system=SYSTEM_PROMPT
    )

    return response.content[0].text, response.usage


def save_weekly_brief(year: int, week_num: int, content: str):
    """Save the weekly brief to the output directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    week_start, week_end = get_week_dates(year, week_num)
    week_label = f"{week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}"

    filename = OUTPUT_DIR / f"{year}-W{week_num:02d}_weekly_brief.md"

    full_content = f"""# Week of {week_label}

{content}
"""

    with open(filename, 'w') as f:
        f.write(full_content)

    print(f"Saved: {filename}")
    return filename


def get_available_weeks() -> list:
    """Get all weeks that have at least one daily brief."""
    weeks = set()

    if not DAILY_BRIEFS_DIR.exists():
        return []

    for brief_file in DAILY_BRIEFS_DIR.glob('*_daily_brief.md'):
        date_str = brief_file.name.split('_')[0]
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            year, week_num, _ = date_obj.isocalendar()
            weeks.add((year, week_num))
        except ValueError:
            continue

    return sorted(weeks)


def main():
    parser = argparse.ArgumentParser(
        description='Generate weekly macro brief from daily briefs'
    )
    parser.add_argument(
        '--week',
        type=str,
        help='Week to generate brief for (YYYY-WNN format, e.g., 2026-W04). Default: latest available.'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate briefs for all available weeks'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing briefs'
    )

    args = parser.parse_args()

    available_weeks = get_available_weeks()

    if not available_weeks:
        print("No daily briefs found.")
        sys.exit(1)

    if args.all:
        weeks_to_process = available_weeks
    elif args.week:
        # Parse YYYY-WNN format
        try:
            year, week_str = args.week.split('-W')
            year = int(year)
            week_num = int(week_str)
            if (year, week_num) not in available_weeks:
                print(f"No daily briefs found for {args.week}")
                print(f"Available weeks: {[f'{y}-W{w:02d}' for y, w in available_weeks[-3:]]}")
                sys.exit(1)
            weeks_to_process = [(year, week_num)]
        except ValueError:
            print("Invalid week format. Use YYYY-WNN (e.g., 2026-W04)")
            sys.exit(1)
    else:
        # Default to latest
        weeks_to_process = [available_weeks[-1]]

    total_cost = 0

    for year, week_num in weeks_to_process:
        output_file = OUTPUT_DIR / f"{year}-W{week_num:02d}_weekly_brief.md"

        if output_file.exists() and not args.force:
            print(f"Skipping {year}-W{week_num:02d} (already exists, use --force to overwrite)")
            continue

        week_start, week_end = get_week_dates(year, week_num)
        week_label = f"{week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}"

        print(f"\n{'='*60}")
        print(f"Generating weekly brief for {year}-W{week_num:02d} ({week_label})")
        print(f"{'='*60}")

        # Load daily briefs
        briefs = load_daily_briefs_for_week(year, week_num)

        if not briefs:
            print(f"No daily briefs found for week {year}-W{week_num:02d}, skipping.")
            continue

        print(f"Found {len(briefs)} daily briefs: {', '.join(sorted(briefs.keys()))}")

        # Generate brief
        try:
            content, usage = generate_weekly_brief(year, week_num, briefs)
            cost = (usage.input_tokens * 0.003 / 1000 + usage.output_tokens * 0.015 / 1000)
            total_cost += cost
            print(f"Generated ({usage.input_tokens} in, {usage.output_tokens} out, ${cost:.4f})")

            # Save
            save_weekly_brief(year, week_num, content)

        except Exception as e:
            print(f"Error generating brief for week {year}-W{week_num:02d}: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"Done! Total cost: ${total_cost:.4f}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
