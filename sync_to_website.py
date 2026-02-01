#!/usr/bin/env python3
"""
Sync briefs from summaries/ to website/ collections for Jekyll.
Converts markdown briefs to Jekyll-compatible format with front matter.
"""
import os
import re
import argparse
from pathlib import Path
from datetime import datetime


SUMMARIES_DIR = Path('summaries')
WEBSITE_DIR = Path('website')

BRIEF_TYPES = {
    'daily': {
        'source': SUMMARIES_DIR / '_daily_briefs',
        'dest': WEBSITE_DIR / '_daily',
        'pattern': r'(\d{4}-\d{2}-\d{2})_daily_brief\.md',
        'date_format': '%Y-%m-%d',
        'title_format': lambda d: d.strftime('%B %d, %Y'),
        'reading_time': 5,
    },
    'weekly': {
        'source': SUMMARIES_DIR / '_weekly_briefs',
        'dest': WEBSITE_DIR / '_weekly',
        'pattern': r'(\d{4})-W(\d{2})_weekly_brief\.md',
        'date_format': 'week',  # Special handling
        'title_format': lambda d: f"Week of {d.strftime('%B %d, %Y')}",
        'reading_time': 8,
    },
    'monthly': {
        'source': SUMMARIES_DIR / '_monthly_briefs',
        'dest': WEBSITE_DIR / '_monthly',
        'pattern': r'(\d{4}-\d{2})_monthly_brief\.md',
        'date_format': '%Y-%m',
        'title_format': lambda d: d.strftime('%B %Y'),
        'reading_time': 12,
    },
}


def get_week_start_date(year: int, week: int) -> datetime:
    """Get the Monday of a given ISO week."""
    jan1 = datetime(year, 1, 1)
    if jan1.isoweekday() <= 4:
        week1_start = jan1 - timedelta(days=jan1.isoweekday() - 1)
    else:
        week1_start = jan1 + timedelta(days=8 - jan1.isoweekday())
    return week1_start + timedelta(weeks=week - 1)


from datetime import timedelta


def extract_lead(content: str) -> str:
    """Extract the lead paragraph from brief content."""
    lines = content.strip().split('\n')

    # Skip the title line (# Date) and any blank lines
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('#'):
            continue
        if not line:
            continue
        # Skip any subtitle lines
        if line.startswith('**') and line.endswith('**'):
            continue
        # This should be the lead paragraph
        if line and not line.startswith('-') and not line.startswith('*'):
            return line

    return ""


def convert_brief(source_file: Path, dest_file: Path, brief_type: str, config: dict):
    """Convert a brief markdown file to Jekyll format."""
    with open(source_file, 'r') as f:
        content = f.read()

    # Parse the filename to get the date
    filename = source_file.name

    if brief_type == 'daily':
        match = re.match(config['pattern'], filename)
        if match:
            date_str = match.group(1)
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    elif brief_type == 'weekly':
        match = re.match(config['pattern'], filename)
        if match:
            year = int(match.group(1))
            week = int(match.group(2))
            date_obj = get_week_start_date(year, week)
            date_str = date_obj.strftime('%Y-%m-%d')
    elif brief_type == 'monthly':
        match = re.match(config['pattern'], filename)
        if match:
            date_str = match.group(1)
            date_obj = datetime.strptime(date_str + '-01', '%Y-%m-%d')
    else:
        return False

    if not match:
        print(f"  Skipping {filename} - doesn't match pattern")
        return False

    # Extract lead paragraph
    lead = extract_lead(content)
    # Escape quotes for YAML
    lead_escaped = lead.replace('"', "'")

    # Remove the title line from content (Jekyll will generate it)
    lines = content.split('\n')
    if lines and lines[0].startswith('# '):
        content = '\n'.join(lines[1:]).strip()

    # Build front matter
    title = config['title_format'](date_obj)
    date_formatted = date_obj.strftime('%Y-%m-%d')
    front_matter = f"""---
layout: brief
title: "{title}"
date: {date_formatted}
brief_type: {brief_type}
reading_time: {config['reading_time']}
lead: "{lead_escaped}"
"""

    if brief_type == 'daily':
        front_matter += f'day_name: "{date_obj.strftime("%A")}"\n'

    front_matter += "---\n\n"

    # Write the Jekyll-formatted file
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_file, 'w') as f:
        f.write(front_matter + content)

    return True


def sync_briefs(brief_type: str = None, force: bool = False):
    """Sync briefs from summaries to website."""
    types_to_sync = [brief_type] if brief_type else BRIEF_TYPES.keys()

    total_synced = 0

    for bt in types_to_sync:
        if bt not in BRIEF_TYPES:
            print(f"Unknown brief type: {bt}")
            continue

        config = BRIEF_TYPES[bt]
        source_dir = config['source']
        dest_dir = config['dest']

        if not source_dir.exists():
            print(f"Source directory not found: {source_dir}")
            continue

        print(f"\nSyncing {bt} briefs...")
        print(f"  From: {source_dir}")
        print(f"  To:   {dest_dir}")

        dest_dir.mkdir(parents=True, exist_ok=True)

        synced = 0
        for source_file in sorted(source_dir.glob('*.md')):
            # Determine destination filename
            if bt == 'daily':
                match = re.match(config['pattern'], source_file.name)
                if match:
                    dest_name = f"{match.group(1)}.md"
            elif bt == 'weekly':
                match = re.match(config['pattern'], source_file.name)
                if match:
                    dest_name = f"{match.group(1)}-W{match.group(2)}.md"
            elif bt == 'monthly':
                match = re.match(config['pattern'], source_file.name)
                if match:
                    dest_name = f"{match.group(1)}.md"
            else:
                continue

            dest_file = dest_dir / dest_name

            # Skip if already exists and not forcing
            if dest_file.exists() and not force:
                # Check if source is newer
                if source_file.stat().st_mtime <= dest_file.stat().st_mtime:
                    continue

            if convert_brief(source_file, dest_file, bt, config):
                print(f"  ✓ {source_file.name} -> {dest_name}")
                synced += 1

        print(f"  Synced {synced} {bt} briefs")
        total_synced += synced

    return total_synced


def main():
    parser = argparse.ArgumentParser(
        description='Sync briefs from summaries/ to website/ for Jekyll'
    )
    parser.add_argument(
        '--type',
        choices=['daily', 'weekly', 'monthly'],
        help='Only sync specific brief type'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force overwrite existing files'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Syncing briefs to website")
    print("=" * 60)

    total = sync_briefs(args.type, args.force)

    print("\n" + "=" * 60)
    print(f"Done! Total synced: {total}")
    print("=" * 60)
    print("\nTo preview the site locally:")
    print("  cd website && bundle exec jekyll serve")


if __name__ == '__main__':
    main()
