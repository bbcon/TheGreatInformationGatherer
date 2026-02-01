#!/usr/bin/env python3
"""
Process content for the knowledge base.
Generates detailed summaries focused on understanding mechanisms and arguments.
"""

import os
import sys
import json
import yaml
import re
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

from src.youtube_handler import YouTubeHandler


def load_knowledge_config():
    """Load knowledge configuration."""
    with open('knowledge/knowledge_config.yaml', 'r') as f:
        return yaml.safe_load(f)


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:80]


def extract_guest_name(title: str) -> str:
    """Extract guest name from episode title."""
    # Common patterns: "Topic | EpXXX: Guest Name" or "Guest Name: Topic | EpXXX"
    if ':' in title:
        parts = title.split(':')
        for part in parts:
            part = part.strip()
            # Skip parts that are episode numbers
            if part.lower().startswith('ep'):
                continue
            # Skip parts with pipe (usually topic descriptions)
            if '|' in part:
                subparts = part.split('|')
                for subpart in subparts:
                    subpart = subpart.strip()
                    if not subpart.lower().startswith('ep') and len(subpart.split()) <= 4:
                        return subpart
            elif len(part.split()) <= 4:  # Likely a name if 4 words or less
                return part
    return "Unknown Guest"


def process_video(video_id: str, title: str, content_type: str = 'podcast',
                  output_folder: str = None, config: dict = None) -> dict:
    """
    Process a single video and generate a knowledge summary.

    Args:
        video_id: YouTube video ID
        title: Video title
        content_type: Type of content (lecture, podcast, paper, book)
        output_folder: Subfolder within knowledge/{type}/ to save to
        config: Knowledge config dict

    Returns:
        Dict with summary info
    """
    if config is None:
        config = load_knowledge_config()

    content_config = config['content_types'].get(content_type, config['content_types']['podcast'])
    prompt_template = content_config['prompt_template']

    # Initialize handlers
    yt = YouTubeHandler(playlist_id='dummy', api_key=os.getenv('YOUTUBE_API_KEY'))
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # Get metadata
    print(f"  Fetching metadata...")
    metadata = yt.get_video_metadata(video_id)

    # Get transcript
    print(f"  Extracting transcript...")
    transcript = yt.get_transcript(video_id)

    if not transcript:
        print(f"  ERROR: Could not extract transcript")
        return None

    print(f"  Transcript: {len(transcript['text'])} chars")

    # Build prompt
    prompt = prompt_template + f"""

CONTENT DETAILS:
Title: {title}
Channel: {metadata.get('channel_title', 'Unknown')}

TRANSCRIPT:
{transcript['text']}
"""

    # Generate summary
    print(f"  Generating summary...")
    response = client.messages.create(
        model=config['defaults']['model'],
        max_tokens=config['defaults']['max_tokens'],
        temperature=config['defaults']['temperature'],
        messages=[{'role': 'user', 'content': prompt}]
    )

    summary_text = response.content[0].text
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    # Cost estimation (Sonnet pricing)
    cost = (input_tokens / 1_000_000 * 3) + (output_tokens / 1_000_000 * 15)

    print(f"  Tokens: {input_tokens:,} in, {output_tokens:,} out (${cost:.2f})")

    # Build output path
    date_str = datetime.now().strftime('%Y-%m-%d')
    guest = extract_guest_name(title)
    slug = slugify(title)

    folder = content_config['folder']
    if output_folder:
        folder = f"{folder}/{output_folder}"

    output_dir = Path('knowledge') / folder
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{date_str}_{slugify(guest)}_{slug[:40]}.md"
    filepath = output_dir / filename

    # Build markdown
    markdown = f"""# {title}

**Guest:** {guest}
**Channel:** {metadata.get('channel_title', 'Unknown')}
**Date Processed:** {date_str}
**Duration:** {metadata.get('duration', 'Unknown')} seconds
**URL:** https://www.youtube.com/watch?v={video_id}

**Tags:** #energy-transition #climate #podcast

---

{summary_text}

---

*Summary generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
*Tokens: {input_tokens:,} input, {output_tokens:,} output | Cost: ${cost:.2f}*
"""

    with open(filepath, 'w') as f:
        f.write(markdown)

    print(f"  Saved: {filepath}")

    return {
        'video_id': video_id,
        'title': title,
        'guest': guest,
        'filepath': str(filepath),
        'summary': summary_text,
        'tokens': {'input': input_tokens, 'output': output_tokens},
        'cost': cost
    }


def process_playlist(playlist_id: str, content_type: str = 'podcast',
                     output_folder: str = None, limit: int = None) -> list:
    """
    Process all videos in a playlist.

    Args:
        playlist_id: YouTube playlist ID
        content_type: Type of content
        output_folder: Subfolder to save to
        limit: Max videos to process (None for all)

    Returns:
        List of summary dicts
    """
    from googleapiclient.discovery import build

    config = load_knowledge_config()
    youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

    # Fetch playlist
    print(f"Fetching playlist {playlist_id}...")
    videos = []
    next_page = None

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            videos.append({'id': video_id, 'title': title})

        next_page = response.get('nextPageToken')
        if not next_page:
            break

    print(f"Found {len(videos)} videos")

    if limit:
        videos = videos[:limit]
        print(f"Processing first {limit} videos")

    # Process each video
    results = []
    total_cost = 0

    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] {video['title'][:60]}...")

        try:
            result = process_video(
                video_id=video['id'],
                title=video['title'],
                content_type=content_type,
                output_folder=output_folder,
                config=config
            )
            if result:
                results.append(result)
                total_cost += result['cost']
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"Processed {len(results)}/{len(videos)} videos")
    print(f"Total cost: ${total_cost:.2f}")
    print(f"{'='*60}")

    return results


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process content for knowledge base')
    parser.add_argument('--video', help='Single video ID to process')
    parser.add_argument('--playlist', help='Playlist ID to process')
    parser.add_argument('--type', default='podcast', choices=['lecture', 'podcast', 'paper', 'book'])
    parser.add_argument('--folder', help='Subfolder within content type folder')
    parser.add_argument('--limit', type=int, help='Max videos to process')
    parser.add_argument('--title', help='Video title (for single video)')

    args = parser.parse_args()

    if args.video:
        result = process_video(
            video_id=args.video,
            title=args.title or 'Unknown',
            content_type=args.type,
            output_folder=args.folder
        )
        print(f"\nDone! Saved to: {result['filepath']}")

    elif args.playlist:
        results = process_playlist(
            playlist_id=args.playlist,
            content_type=args.type,
            output_folder=args.folder,
            limit=args.limit
        )

    else:
        print("Please provide --video or --playlist")
        sys.exit(1)
