#!/usr/bin/env python3
"""
Helper script to extract video ID from a YouTube URL or playlist.
"""
import sys
import re


def extract_video_id(url: str) -> str:
    """
    Extract video ID from various YouTube URL formats.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - Or just the video ID directly
    """
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'  # Direct video ID
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def main():
    print("=" * 70)
    print("YouTube Video ID Extractor")
    print("=" * 70)
    print()

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("Instructions:")
        print("1. Open your YouTube playlist in a browser:")
        print("   https://www.youtube.com/playlist?list=PLGaYlBJIOoa_vIH-o9MQZHg86xdx496BW")
        print()
        print("2. Click on the FIRST video in the playlist (the latest one)")
        print()
        print("3. Copy the URL from your browser's address bar")
        print()
        url = input("Paste the video URL here: ").strip()

    if not url:
        print("No URL provided. Exiting.")
        sys.exit(1)

    video_id = extract_video_id(url)

    if video_id:
        print()
        print("=" * 70)
        print(f"✓ Video ID: {video_id}")
        print("=" * 70)
        print()
        print("Now run:")
        print(f"  python3 main.py --video-id {video_id}")
        print()
        print("Or to skip email:")
        print(f"  python3 main.py --video-id {video_id} --no-email")
        print()
    else:
        print()
        print("✗ Could not extract video ID from the provided URL.")
        print()
        print("Please make sure you're providing a valid YouTube video URL like:")
        print("  https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        sys.exit(1)


if __name__ == '__main__':
    main()
