#!/usr/bin/env python3
"""
Process missing Bloomberg videos from Jan 14-30.
"""
import subprocess
import time
import sys

# Missing videos by show (one video per date to avoid duplicates)
MISSING_VIDEOS = {
    'bloomberg_brief': [
        ('2026-01-15', '95cLDY_XgGk'),
        ('2026-01-22', 'kgw0k7TcMX0'),
        ('2026-01-26', 'n5wx3TRrqrE'),
        ('2026-01-29', '407GSocCN9Q'),
    ],
    'bloomberg_surveillance': [
        ('2026-01-14', 's7dcsn0x13I'),
        ('2026-01-20', 'dPWayUgKUf4'),
        ('2026-01-22', '095j7KNUNTQ'),
        ('2026-01-26', 'U032IFNvPOA'),
        ('2026-01-28', '5sCovV5T3RM'),  # Main show for Jan 28
        ('2026-01-29', 'GpDFucVLt7w'),
    ],
    'daybreak_europe': [
        ('2026-01-26', '6Nc-9yaZVRc'),  # First Jan 26
        ('2026-01-28', 'ZrGoM7Pk9PY'),
        ('2026-01-29', '9O8Dnc0aTcU'),  # First Jan 29
    ],
    'the_china_show': [
        ('2026-01-26', 'ClHn_u6UPX8'),
        ('2026-01-29', 'Aso7d66Ym5Y'),
        ('2026-01-30', 'Xk_3cpDe2so'),
    ],
    'the_close': [
        ('2026-01-17', 'cU-PFQ-QLzA'),
        ('2026-01-20', 'H49iuONyaVw'),  # First Jan 20
        ('2026-01-26', 'CPi92PG9BY0'),  # First Jan 26
        ('2026-01-29', '6xz6KoJYxFI'),  # Main Close for Jan 29
    ],
}

def process_video(show_key: str, video_id: str, date: str) -> bool:
    """Process a single video."""
    print(f"\n{'='*70}")
    print(f"Processing {show_key} - {date} - {video_id}")
    print(f"{'='*70}")

    # Handle video IDs starting with -
    if video_id.startswith('-'):
        cmd = [
            'python3', 'process_show.py', show_key,
            f'--video-id={video_id}',
            '--no-email',
            '--force'
        ]
    else:
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
    print(f"Successful: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")

    if results['failed']:
        print("\nFailed videos:")
        for show, date, vid in results['failed']:
            print(f"  - {show} | {date} | {vid}")

if __name__ == '__main__':
    main()
