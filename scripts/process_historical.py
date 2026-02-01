#!/usr/bin/env python3
"""
Process historical Bloomberg videos by video ID.
Usage: python3 process_historical.py
"""
import subprocess
import time
import sys

# Define all missing videos by show
MISSING_VIDEOS = {
    'bloomberg_brief': [
        ('2026-01-05', 'ISN6SjPaKGE'),
        ('2026-01-06', 'agWe4a-mKdk'),  # First Jan 6 video
        ('2026-01-07', '4yyelfkwWUU'),
        ('2026-01-08', 'pyAL6Kcu_Rk'),
        ('2026-01-09', '0_fu0oWA9gI'),
        ('2026-01-12', 'emOSv5hRPOI'),
        ('2026-01-13', 'MF3ywfAWVuE'),
    ],
    'bloomberg_surveillance': [
        ('2026-01-02', 'cr5h6UajH-M'),
        ('2026-01-05', '-Sq1NwXp5tA'),
        ('2026-01-06', 'tKoIspAk9Xk'),
        ('2026-01-07', 'sMoctvqYCWg'),
        ('2026-01-08', 'YBUxuzb4Ljg'),
        ('2026-01-09', 'b2vM2DHKGw0'),
        ('2026-01-12', 'goPceTcDNh8'),
        ('2026-01-13', 'cxvswT7eDwE'),
    ],
    'daybreak_europe': [
        ('2026-01-05', 'EqXtLkCGpz8'),  # First Jan 5
        ('2026-01-06', 'MJCbmEbowmk'),  # First Jan 6
        ('2026-01-07', 'GcN4G9IJUXw'),  # First Jan 7
        ('2026-01-08', 'knXSr6a_RrI'),  # First Jan 8
        ('2026-01-09', 'FLRvrUwTPVY'),  # First Jan 9
        ('2026-01-12', 'GIHiE8I6sMI'),  # First Jan 12
        ('2026-01-13', 'o16RuudCp7E'),  # First Jan 13
    ],
    'the_china_show': [
        ('2026-01-05', 'r8wfwoHc4XQ'),
        ('2026-01-06', '0l4KDcKDklU'),  # Main show Jan 6
        ('2026-01-07', '3jlIad-a1g0'),
        ('2026-01-08', '1TAn_8CBQmU'),
        ('2026-01-09', 'iQW0JnBKGlk'),  # First Jan 9
        ('2026-01-12', 'nGua571SRYE'),
        ('2026-01-13', 'wIOHh2e77_I'),  # Main show Jan 13
    ],
    'the_close': [
        ('2026-01-05', 'CoGwBM3qiso'),
        ('2026-01-06', '233nXK9TmV8'),  # First Jan 6
        ('2026-01-07', '-htgmoaCraU'),  # First Jan 7
        ('2026-01-08', 'ytWeP7Y5HGo'),  # First Jan 8
        ('2026-01-09', '7D8jj0ZofyA'),
        ('2026-01-10', 'f5wMclRcG5Q'),
        ('2026-01-12', '57Lmj6zm0MQ'),  # First Jan 12
        ('2026-01-13', 'FFfZrHqk-bM'),  # First Jan 13
    ],
}

def process_video(show_key: str, video_id: str, date: str) -> bool:
    """Process a single video."""
    print(f"\n{'='*70}")
    print(f"Processing {show_key} - {date} - {video_id}")
    print(f"{'='*70}")

    cmd = [
        'python3', 'process_show.py', show_key,
        '--video-id', video_id,
        '--no-email',
        '--force'
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        print(result.stdout)
        if result.returncode != 0:
            print(f"STDERR: {result.stderr}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"ERROR: Timeout processing {video_id}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    # Process specific show if provided
    if len(sys.argv) > 1:
        show_filter = sys.argv[1]
        shows_to_process = {k: v for k, v in MISSING_VIDEOS.items() if k == show_filter}
    else:
        shows_to_process = MISSING_VIDEOS

    results = {'success': [], 'failed': []}

    for show_key, videos in shows_to_process.items():
        print(f"\n{'#'*70}")
        print(f"# Starting {show_key} ({len(videos)} videos)")
        print(f"{'#'*70}")

        for date, video_id in videos:
            success = process_video(show_key, video_id, date)
            if success:
                results['success'].append((show_key, date, video_id))
            else:
                results['failed'].append((show_key, date, video_id))

            # Small delay to avoid rate limits
            time.sleep(2)

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"✓ Successful: {len(results['success'])}")
    print(f"✗ Failed: {len(results['failed'])}")

    if results['failed']:
        print("\nFailed videos:")
        for show, date, vid in results['failed']:
            print(f"  - {show} | {date} | {vid}")

if __name__ == '__main__':
    main()
