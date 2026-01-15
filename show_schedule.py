#!/usr/bin/env python3
"""
Display the schedule for all configured shows and generate cron entries.
"""
import yaml
from pathlib import Path
from datetime import datetime, timedelta
import sys

def load_shows_config():
    """Load shows configuration from YAML."""
    config_path = Path(__file__).parent / 'shows_config.yaml'
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def time_to_cron(time_str, delay_minutes=0):
    """Convert HH:MM time to cron expression with delay."""
    hour, minute = map(int, time_str.split(':'))

    # Add delay
    total_minutes = hour * 60 + minute + delay_minutes
    final_hour = (total_minutes // 60) % 24
    final_minute = total_minutes % 60

    return final_minute, final_hour

def days_to_cron(days):
    """Convert day names to cron day-of-week format."""
    day_map = {
        'monday': '1',
        'tuesday': '2',
        'wednesday': '3',
        'thursday': '4',
        'friday': '5',
        'saturday': '6',
        'sunday': '0'
    }

    day_numbers = [day_map[day.lower()] for day in days if day.lower() in day_map]
    return ','.join(day_numbers) if day_numbers else '*'

def main():
    config = load_shows_config()

    print("=" * 80)
    print("BLOOMBERG SHOWS SCHEDULE")
    print("=" * 80)

    for show_key, show_config in config['shows'].items():
        if not show_config.get('enabled', True):
            continue

        print(f"\n{show_config['name']}")
        print("-" * 80)

        if 'publish_schedule' not in show_config:
            print("  No schedule configured")
            continue

        schedule = show_config['publish_schedule']
        days = schedule.get('days', [])
        pub_time = schedule.get('time', 'N/A')
        timezone = schedule.get('timezone', 'UTC')
        delay = show_config.get('fetch_delay_minutes', 0)

        # Calculate fetch time
        if ':' in pub_time:
            hour, minute = map(int, pub_time.split(':'))
            pub_dt = datetime.now().replace(hour=hour, minute=minute, second=0)
            fetch_dt = pub_dt + timedelta(minutes=delay)
            fetch_time = fetch_dt.strftime('%H:%M')
        else:
            fetch_time = 'N/A'

        print(f"  Publish Time: {pub_time} {timezone}")
        print(f"  Fetch Delay: {delay} minutes")
        print(f"  Fetch Time: {fetch_time} {timezone}")
        print(f"  Days: {', '.join(days)}")
        print(f"  Command: python3 process_show.py {show_key}")

    print("\n" + "=" * 80)
    print("CRON SCHEDULE (for automated runs)")
    print("=" * 80)
    print("\nAdd these to your crontab or use GitHub Actions:\n")

    for show_key, show_config in config['shows'].items():
        if not show_config.get('enabled', True):
            continue

        if 'publish_schedule' not in show_config:
            continue

        schedule = show_config['publish_schedule']
        pub_time = schedule.get('time', '')
        days = schedule.get('days', [])
        delay = show_config.get('fetch_delay_minutes', 0)

        if not pub_time or not days:
            continue

        minute, hour = time_to_cron(pub_time, delay)
        dow = days_to_cron(days)

        cron_expr = f"{minute} {hour} * * {dow}"

        print(f"# {show_config['name']}")
        print(f"{cron_expr} cd /path/to/repo && python3 process_show.py {show_key}")
        print()

    print("=" * 80)
    print("\nNotes:")
    print("- Times shown are in UTC for cron")
    print("- Adjust paths in cron commands to your actual repository location")
    print("- For local machine, use crontab -e to edit your cron schedule")
    print("- For GitHub Actions, see .github/workflows/ for automation")
    print("=" * 80)

if __name__ == '__main__':
    main()
