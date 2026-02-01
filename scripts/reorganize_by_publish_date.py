#!/usr/bin/env python3
"""
Reorganize summary files by their video publication date instead of processing date.
Reads the published_at field from JSON files and moves files to correct date folders.
"""
import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# Shows to process
SHOWS = [
    'bloomberg_brief',
    'bloomberg_surveillance',
    'daybreak_europe',
    'the_china_show',
    'the_close'
]

def get_publish_date(json_path: Path) -> str:
    """Extract publication date from JSON file."""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        pub_str = data.get('video_metadata', {}).get('published_at', '')

        if len(pub_str) == 8 and pub_str.isdigit():
            # Format: YYYYMMDD -> YYYY-MM-DD
            return f"{pub_str[:4]}-{pub_str[4:6]}-{pub_str[6:8]}"
        elif 'T' in pub_str:
            # ISO format
            dt = datetime.fromisoformat(pub_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d')

        return None
    except Exception as e:
        print(f"  Error reading {json_path}: {e}")
        return None

def reorganize_show(show_name: str, summaries_dir: Path, dry_run: bool = False):
    """Reorganize a single show's summaries by publication date."""
    show_dir = summaries_dir / show_name

    if not show_dir.exists():
        print(f"  Show directory not found: {show_dir}")
        return

    moves = []

    # Find all date folders
    for date_folder in sorted(show_dir.iterdir()):
        if not date_folder.is_dir() or date_folder.name.startswith('.'):
            continue

        current_date = date_folder.name  # e.g., "2026-01-30"

        # Find JSON files in this folder
        json_files = list(date_folder.glob('*.json'))

        for json_file in json_files:
            publish_date = get_publish_date(json_file)

            if not publish_date:
                print(f"  Could not determine publish date for: {json_file.name}")
                continue

            if publish_date != current_date:
                # Need to move this file
                md_file = json_file.with_suffix('.md')
                moves.append({
                    'json': json_file,
                    'md': md_file if md_file.exists() else None,
                    'from_date': current_date,
                    'to_date': publish_date
                })

    if not moves:
        print(f"  No files need moving for {show_name}")
        return

    print(f"\n  Found {len(moves)} file(s) to move:")

    for move in moves:
        print(f"    {move['json'].name}: {move['from_date']} -> {move['to_date']}")

        if not dry_run:
            # Create target directory
            target_dir = show_dir / move['to_date']
            target_dir.mkdir(parents=True, exist_ok=True)

            # Move JSON file
            target_json = target_dir / move['json'].name
            shutil.move(str(move['json']), str(target_json))

            # Move MD file if exists
            if move['md'] and move['md'].exists():
                target_md = target_dir / move['md'].name
                shutil.move(str(move['md']), str(target_md))

            # Remove old folder if empty
            old_dir = show_dir / move['from_date']
            if old_dir.exists() and not any(old_dir.iterdir()):
                old_dir.rmdir()
                print(f"    Removed empty folder: {move['from_date']}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Reorganize summaries by publication date')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be moved without actually moving')
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent
    summaries_dir = base_dir / 'summaries'

    print("Reorganizing summaries by publication date...")
    print(f"Base directory: {summaries_dir}")

    if args.dry_run:
        print("\n*** DRY RUN - No files will be moved ***\n")

    for show in SHOWS:
        print(f"\nProcessing: {show}")
        reorganize_show(show, summaries_dir, dry_run=args.dry_run)

    print("\nDone!")

if __name__ == '__main__':
    main()
