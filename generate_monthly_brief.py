#!/usr/bin/env python3
"""
Generate a monthly macro brief by combining weekly briefs.
Provides a hindsight view of what really mattered during the month.
"""
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from calendar import monthrange
from dotenv import load_dotenv
import anthropic

load_dotenv()

WEEKLY_BRIEFS_DIR = Path('summaries/_weekly_briefs')
OUTPUT_DIR = Path('summaries/_monthly_briefs')

SYSTEM_PROMPT = """You are writing a monthly macro brief for a professional audience of macro strategists and portfolio managers. Synthesize the month's developments into a measured, analytical summary.

TONE:
- Write like a Goldman Sachs research note, not a news article
- Be measured and analytical. Understate rather than overstate.
- Use strong words (historic, unprecedented, crisis) ONLY when truly justified - a routine 2% market move is not "dramatic"
- Default to neutral language: fell, rose, declined, gained, increased, decreased
- Let data speak: "gold fell 8%" is impactful on its own - you don't need to add "worst since 1983"
- The numbers ARE the story. Superlatives should be rare and earned.
- Readers are sophisticated professionals who find unnecessary hyperbole off-putting

MACRO CONSISTENCY:
- Ensure all narratives are logically consistent
- Example: If "Fed independence under threat" means pressure for LOWER rates (dovish), then nominating a hawkish chair like Warsh contradicts or complicates that narrative - acknowledge the tension rather than presenting both as threats
- Think through cause and effect: policy X should logically lead to market reaction Y
- Don't combine contradictory narratives - either reconcile them or note the apparent contradiction

ACKNOWLEDGE UNCERTAINTY:
- Reality is messy - avoid false narrative closure
- Don't declare crises "resolved" when outcomes remain uncertain - e.g., a nomination doesn't resolve political tensions, it just shifts them
- Use hedging language where appropriate: "appears to," "may signal," "remains to be seen"
- Avoid the temptation to wrap everything into a neat story - sometimes things are genuinely unclear
- Distinguish between what happened (facts) and what it means (interpretation that may prove wrong)

GUIDELINES:
- Identify 4-6 themes that defined the month
- Distinguish signal from noise - what actually mattered vs what seemed important at the time
- Use specific numbers and data points
- Track how narratives evolved across the month
- Report facts, let readers draw conclusions
- Do NOT mention Bloomberg, TV shows, or any source attribution

STRUCTURE:
- Start with a 2-3 sentence lead summarizing the month's key developments (not dramatic framing)
- Use **bold section headers** for each theme (4-6 themes)
- Within each section:
  - Brief context (1-2 sentences)
  - Bullet points for specific data and developments (use "-" for bullets)
- Include a brief "Looking Ahead" section
- Target ~1500 words
- IMPORTANT: Always leave a blank line before starting a bullet list

WHAT TO INCLUDE:
- Persistent trends that shaped market dynamics
- Policy developments and central bank actions
- Meaningful sector rotations or leadership changes
- Geopolitical developments with market implications

WHAT TO CUT:
- Intraday or single-day noise that reversed
- Headlines that didn't ultimately matter
- Dramatic framing of normal market volatility
"""

USER_PROMPT_TEMPLATE = """Here are the weekly macro briefs for {month_label}. Synthesize these into a monthly brief that identifies what really mattered - cutting through the noise to highlight the key themes and developments that defined the month.

{weekly_briefs}

Generate the monthly brief now. Identify 4-6 major themes that truly defined the month, ~1500 words. Use bullet points liberally within each section for key data and developments."""


def get_month_weeks(year: int, month: int) -> list:
    """Get all ISO week numbers that fall within a given month."""
    weeks = set()

    # Get first and last day of month
    _, last_day = monthrange(year, month)

    for day in range(1, last_day + 1):
        date_obj = datetime(year, month, day)
        iso_year, week_num, _ = date_obj.isocalendar()
        # Only include weeks where the Thursday falls in this month
        # (ISO week belongs to the year/month containing its Thursday)
        thursday = date_obj
        while thursday.weekday() != 3:  # Find Thursday of this week
            thursday = datetime(year, month, day)
            break
        weeks.add((iso_year, week_num))

    return sorted(weeks)


def load_weekly_briefs_for_month(year: int, month: int) -> dict:
    """Load all weekly briefs for a given month."""
    briefs = {}

    # Get all weeks that might overlap with this month
    _, last_day = monthrange(year, month)

    checked_weeks = set()
    for day in range(1, last_day + 1):
        date_obj = datetime(year, month, day)
        iso_year, week_num, _ = date_obj.isocalendar()

        if (iso_year, week_num) in checked_weeks:
            continue
        checked_weeks.add((iso_year, week_num))

        brief_file = WEEKLY_BRIEFS_DIR / f"{iso_year}-W{week_num:02d}_weekly_brief.md"

        if brief_file.exists():
            with open(brief_file, 'r') as f:
                content = f.read()
                # Remove the week header line
                lines = content.split('\n')
                if lines and lines[0].startswith('# Week of'):
                    content = '\n'.join(lines[1:]).strip()
                briefs[f"{iso_year}-W{week_num:02d}"] = content

    return briefs


def generate_monthly_brief(year: int, month: int, briefs: dict) -> str:
    """Use Claude to generate the monthly brief."""
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    month_label = datetime(year, month, 1).strftime('%B %Y')

    # Format weekly briefs
    briefs_text = ""
    for week_key in sorted(briefs.keys()):
        briefs_text += f"\n\n=== {week_key} ===\n{briefs[week_key]}"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=6000,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(
                    month_label=month_label,
                    weekly_briefs=briefs_text
                )
            }
        ],
        system=SYSTEM_PROMPT
    )

    return response.content[0].text, response.usage


def save_monthly_brief(year: int, month: int, content: str):
    """Save the monthly brief to the output directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    month_label = datetime(year, month, 1).strftime('%B %Y')

    filename = OUTPUT_DIR / f"{year}-{month:02d}_monthly_brief.md"

    full_content = f"""# {month_label}

{content}
"""

    with open(filename, 'w') as f:
        f.write(full_content)

    print(f"Saved: {filename}")
    return filename


def get_available_months() -> list:
    """Get all months that have at least one weekly brief."""
    months = set()

    if not WEEKLY_BRIEFS_DIR.exists():
        return []

    for brief_file in WEEKLY_BRIEFS_DIR.glob('*_weekly_brief.md'):
        # Parse YYYY-WNN format
        name = brief_file.stem.replace('_weekly_brief', '')
        try:
            year, week_str = name.split('-W')
            year = int(year)
            week_num = int(week_str)

            # Find the month this week belongs to (use Thursday)
            jan1 = datetime(year, 1, 1)
            if jan1.isoweekday() <= 4:
                week1_start = jan1 - timedelta(days=jan1.isoweekday() - 1)
            else:
                week1_start = jan1 + timedelta(days=8 - jan1.isoweekday())

            week_start = week1_start + timedelta(weeks=week_num - 1)
            thursday = week_start + timedelta(days=3)

            months.add((thursday.year, thursday.month))
        except (ValueError, IndexError):
            continue

    return sorted(months)


from datetime import timedelta

def main():
    parser = argparse.ArgumentParser(
        description='Generate monthly macro brief from weekly briefs'
    )
    parser.add_argument(
        '--month',
        type=str,
        help='Month to generate brief for (YYYY-MM format, e.g., 2026-01). Default: latest available.'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate briefs for all available months'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing briefs'
    )

    args = parser.parse_args()

    available_months = get_available_months()

    if not available_months:
        print("No weekly briefs found.")
        sys.exit(1)

    if args.all:
        months_to_process = available_months
    elif args.month:
        # Parse YYYY-MM format
        try:
            year, month = args.month.split('-')
            year = int(year)
            month = int(month)
            months_to_process = [(year, month)]
        except ValueError:
            print("Invalid month format. Use YYYY-MM (e.g., 2026-01)")
            sys.exit(1)
    else:
        # Default to latest
        months_to_process = [available_months[-1]]

    total_cost = 0

    for year, month in months_to_process:
        output_file = OUTPUT_DIR / f"{year}-{month:02d}_monthly_brief.md"

        if output_file.exists() and not args.force:
            print(f"Skipping {year}-{month:02d} (already exists, use --force to overwrite)")
            continue

        month_label = datetime(year, month, 1).strftime('%B %Y')

        print(f"\n{'='*60}")
        print(f"Generating monthly brief for {month_label}")
        print(f"{'='*60}")

        # Load weekly briefs
        briefs = load_weekly_briefs_for_month(year, month)

        if not briefs:
            print(f"No weekly briefs found for {month_label}, skipping.")
            continue

        print(f"Found {len(briefs)} weekly briefs: {', '.join(sorted(briefs.keys()))}")

        # Generate brief
        try:
            content, usage = generate_monthly_brief(year, month, briefs)
            cost = (usage.input_tokens * 0.003 / 1000 + usage.output_tokens * 0.015 / 1000)
            total_cost += cost
            print(f"Generated ({usage.input_tokens} in, {usage.output_tokens} out, ${cost:.4f})")

            # Save
            save_monthly_brief(year, month, content)

        except Exception as e:
            print(f"Error generating brief for {month_label}: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"Done! Total cost: ${total_cost:.4f}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
