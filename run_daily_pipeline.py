#!/usr/bin/env python3
"""
Daily pipeline: Process all Bloomberg shows and generate daily brief.

Schedule: Run at 14:00 UTC (9:00 AM ET / 3:00 PM CET) Mon-Fri

Logic:
- Today's brief includes: The Close (yesterday) + morning shows (today)
- Example: Tuesday's brief = The Close (Mon) + China/Daybreak/Surveillance/Brief (Tue)

Cron:
    0 14 * * 1-5 cd /path/to/TheGreatInformationGatherer && python3 run_daily_pipeline.py
"""
import os
import sys
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = Path(__file__).parent
LOG_DIR = PROJECT_DIR / 'logs'

# Morning shows (process for today)
MORNING_SHOWS = [
    'the_china_show',
    'daybreak_europe',
    'bloomberg_surveillance',
    'bloomberg_brief',
]

# Evening show (process for yesterday, include in today's brief)
EVENING_SHOW = 'the_close'


def log(message: str):
    """Print timestamped log message."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")


def run_command(cmd: list, description: str) -> bool:
    """Run a command and return success status."""
    log(f"Running: {description}")
    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout per command
        )
        if result.returncode == 0:
            log(f"  ✓ {description} completed")
            return True
        else:
            log(f"  ✗ {description} failed: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        log(f"  ✗ {description} timed out")
        return False
    except Exception as e:
        log(f"  ✗ {description} error: {e}")
        return False


def is_weekday(date_str: str) -> bool:
    """Check if date is a weekday (shows only air Mon-Fri)."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.weekday() < 5  # 0-4 = Mon-Fri


def get_previous_trading_day(date_str: str) -> str:
    """Get the previous trading day (skips weekends)."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    prev_day = date_obj - timedelta(days=1)

    # Skip backwards over weekends
    while prev_day.weekday() >= 5:  # Saturday=5, Sunday=6
        prev_day -= timedelta(days=1)

    return prev_day.strftime('%Y-%m-%d')


def main():
    LOG_DIR.mkdir(exist_ok=True)

    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    prev_trading_day = get_previous_trading_day(today)

    log("=" * 60)
    log(f"Daily Pipeline")
    log(f"  Today's date: {today}")
    log(f"  The Close from: {prev_trading_day}")
    log("=" * 60)

    # Check if today is weekday
    if not is_weekday(today):
        log(f"Skipping - {today} is a weekend (no shows)")
        return

    shows_processed = 0

    # 1. Process The Close from previous trading day
    log(f"\n--- Processing The Close from {prev_trading_day} ---")
    success = run_command(
        [sys.executable, 'process_show.py', EVENING_SHOW, '--no-email'],
        f"Process {EVENING_SHOW} ({prev_trading_day})"
    )
    if success:
        shows_processed += 1

    # 2. Process morning shows for today
    log(f"\n--- Processing morning shows for {today} ---")
    for show in MORNING_SHOWS:
        success = run_command(
            [sys.executable, 'process_show.py', show, '--no-email'],
            f"Process {show}"
        )
        if success:
            shows_processed += 1

    log(f"\nProcessed {shows_processed} shows total")

    if shows_processed == 0:
        log("No shows processed - skipping daily brief")
        return

    # 3. Generate daily brief for today
    run_command(
        [sys.executable, 'generate_daily_brief.py', '--date', today],
        f"Generate daily brief for {today}"
    )

    # 4. Send daily brief email
    run_command(
        [sys.executable, 'send_briefs.py', '--daily', today],
        f"Send daily brief email for {today}"
    )

    # 5. Sync to website
    run_command(
        [sys.executable, 'sync_to_website.py'],
        "Sync to website"
    )

    # 6. Check if it's end of week (Friday) - generate weekly brief
    date_obj = datetime.strptime(today, '%Y-%m-%d')
    if date_obj.weekday() == 4:  # Friday
        year, week, _ = date_obj.isocalendar()
        week_str = f'{year}-W{week:02d}'
        run_command(
            [sys.executable, 'generate_weekly_brief.py', '--week', week_str, '--force'],
            f"Generate weekly brief for {week_str}"
        )
        run_command(
            [sys.executable, 'send_briefs.py', '--weekly', week_str],
            f"Send weekly brief email for {week_str}"
        )

    # 7. Check if it's end of month - generate monthly brief
    # Case 1: Today is last weekday of month (tomorrow is different month)
    tomorrow = date_obj + timedelta(days=1)
    monthly_generated = None
    if tomorrow.month != date_obj.month:
        monthly_generated = date_obj.strftime('%Y-%m')
        run_command(
            [sys.executable, 'generate_monthly_brief.py', '--month', monthly_generated, '--force'],
            f"Generate monthly brief for {date_obj.strftime('%B %Y')}"
        )
    # Case 2: First Monday of new month - catch weekend month-ends
    elif date_obj.day <= 3 and date_obj.weekday() == 0:  # Monday, day 1-3
        prev_month_last_day = date_obj.replace(day=1) - timedelta(days=1)
        if prev_month_last_day.weekday() >= 5:  # Previous month ended on Sat/Sun
            monthly_generated = prev_month_last_day.strftime('%Y-%m')
            run_command(
                [sys.executable, 'generate_monthly_brief.py', '--month', monthly_generated, '--force'],
                f"Generate monthly brief for {prev_month_last_day.strftime('%B %Y')}"
            )

    # Note: Monthly email not yet implemented in send_briefs.py
    # if monthly_generated:
    #     run_command(
    #         [sys.executable, 'send_briefs.py', '--monthly', monthly_generated],
    #         f"Send monthly brief email for {monthly_generated}"
    #     )

    # 8. Push to GitHub (updates GitHub Pages)
    log(f"\n--- Pushing to GitHub ---")
    run_command(
        ['git', 'add', 'website/_daily/', 'website/_weekly/', 'website/_monthly/'],
        "Stage changes"
    )
    run_command(
        ['git', 'commit', '-m', f'Daily brief for {today}'],
        "Commit changes"
    )
    run_command(
        ['git', 'push'],
        "Push to GitHub"
    )

    log("\n" + "=" * 60)
    log("Pipeline complete!")
    log("=" * 60)


if __name__ == '__main__':
    main()
