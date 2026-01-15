#!/usr/bin/env python3
"""
Process a single Bloomberg show by name.
Usage: python3 process_show.py bloomberg_brief
"""
import os
import sys
import yaml
import argparse
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from youtube_handler import YouTubeHandler
from summarizer_v2 import MacroTradingSummarizer
from output_manager import OutputManager
from email_sender import EmailSender
from config_handler import ConfigHandler

def load_shows_config():
    """Load shows configuration from YAML."""
    config_path = Path(__file__).parent / 'shows_config.yaml'
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def check_if_processed(video_id: str, state_file: str) -> bool:
    """Check if video was already processed."""
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return f.read().strip() == video_id
    return False

def mark_as_processed(video_id: str, state_file: str):
    """Mark video as processed."""
    with open(state_file, 'w') as f:
        f.write(video_id)

def process_show(show_key: str, force: bool = False, send_email: bool = True):
    """Process a single show."""
    load_dotenv()

    # Load configuration
    config = load_shows_config()

    if show_key not in config['shows']:
        print(f"Error: Show '{show_key}' not found in configuration.")
        print(f"Available shows: {', '.join(config['shows'].keys())}")
        sys.exit(1)

    show_config = config['shows'][show_key]

    if not show_config.get('enabled', True):
        print(f"Show '{show_key}' is disabled in configuration.")
        sys.exit(0)

    print("=" * 70)
    print(f"Processing: {show_config['name']}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Initialize handlers
    yt_handler = YouTubeHandler(
        playlist_id=show_config['playlist_id'],
        api_key=os.getenv('YOUTUBE_API_KEY')
    )

    # Get latest video
    print(f"\n[1/6] Fetching latest video...")
    video_id = yt_handler.get_latest_video_id()

    if not video_id:
        print("✗ Could not fetch latest video ID")
        sys.exit(1)

    print(f"✓ Found video: {video_id}")

    # Check if already processed
    if not force and check_if_processed(video_id, show_config['state_file']):
        print(f"\n✓ Video already processed. Use --force to reprocess.")
        sys.exit(0)

    # Get metadata
    print(f"\n[2/6] Fetching metadata...")
    metadata = yt_handler.get_video_metadata(video_id)

    if metadata:
        print(f"✓ Title: {metadata.get('title', 'N/A')}")
        print(f"  Channel: {metadata.get('channel_title', 'N/A')}")
        print(f"  Published: {metadata.get('published_at', 'N/A')}")

    # Get transcript
    print(f"\n[3/6] Extracting transcript...")
    transcript_data = yt_handler.get_transcript(video_id)

    if not transcript_data:
        print("✗ Could not extract transcript")
        sys.exit(1)

    print(f"✓ Transcript extracted ({len(transcript_data['text'])} characters)")
    print(f"  Language: {transcript_data['language']}")

    # Save transcript
    yt_handler.save_transcript(transcript_data)

    # Generate summary
    print(f"\n[4/6] Generating summary with Claude...")
    summarizer = MacroTradingSummarizer(api_key=os.getenv('ANTHROPIC_API_KEY'))

    try:
        summary_data = summarizer.generate_summary(
            transcript=transcript_data['text'],
            video_metadata=metadata
        )
        print(f"✓ Summary generated!")
        print(f"  Input tokens: {summary_data['tokens_used']['input']}")
        print(f"  Output tokens: {summary_data['tokens_used']['output']}")
        cost = (summary_data['tokens_used']['input'] * 0.003 / 1000 +
                summary_data['tokens_used']['output'] * 0.015 / 1000)
        print(f"  Estimated cost: ${cost:.4f}")

    except Exception as e:
        print(f"✗ Summary generation failed: {e}")
        sys.exit(1)

    # Save summary
    print(f"\n[5/6] Saving summary files...")
    markdown_content = summarizer.format_as_markdown(summary_data)

    # Get folder structure from config
    config_handler = ConfigHandler()
    folder_structure = config_handler.get_folder_structure()

    output_manager = OutputManager(
        folder_structure=folder_structure,
        show_name=show_key
    )
    saved_files = output_manager.save_summary(summary_data, markdown_content)

    print(f"✓ Files saved:")
    for file_type, file_path in saved_files.items():
        print(f"  {file_type}: {file_path}")

    # Send email
    if send_email:
        print(f"\n[6/6] Sending email...")

        if not all([os.getenv('SMTP_SERVER'), os.getenv('SMTP_USERNAME'),
                    os.getenv('SMTP_PASSWORD'), os.getenv('EMAIL_TO')]):
            print("⚠️  Email not configured. Skipping.")
        else:
            sender = EmailSender(
                smtp_server=os.getenv('SMTP_SERVER'),
                smtp_port=int(os.getenv('SMTP_PORT', 587)),
                username=os.getenv('SMTP_USERNAME'),
                password=os.getenv('SMTP_PASSWORD'),
                from_address=os.getenv('EMAIL_FROM')
            )

            email_html = summarizer.format_email_body(summary_data)
            subject = f"📊 {show_config['name']} Summary - {metadata.get('title', '')[:50]}"

            success = sender.send_summary(
                to_address=os.getenv('EMAIL_TO'),
                subject=subject,
                html_body=email_html,
                plain_text_body=summary_data['summary']
            )

            if success:
                print("✓ Email sent successfully!")
            else:
                print("✗ Failed to send email")
    else:
        print(f"\n[6/6] Email skipped (--no-email flag)")

    # Mark as processed
    mark_as_processed(video_id, show_config['state_file'])

    print("\n" + "=" * 70)
    print("✓ Complete!")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(
        description='Process a single Bloomberg show',
        epilog='Example: python3 process_show.py bloomberg_brief'
    )
    parser.add_argument(
        'show',
        help='Show key from shows_config.yaml (e.g., bloomberg_brief)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force reprocessing even if already processed'
    )
    parser.add_argument(
        '--no-email',
        action='store_true',
        help='Skip sending email'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all configured shows'
    )

    args = parser.parse_args()

    if args.list or args.show == 'list':
        config = load_shows_config()
        print("\nConfigured Shows:")
        print("=" * 70)
        for show_key, show_config in config['shows'].items():
            status = "✓ enabled" if show_config.get('enabled', True) else "✗ disabled"
            print(f"\n{show_key}: {show_config['name']} ({status})")
            if 'publish_schedule' in show_config:
                days = ', '.join(show_config['publish_schedule'].get('days', []))
                time = show_config['publish_schedule'].get('time', 'N/A')
                print(f"  Schedule: {days} at {time}")
        print("\n" + "=" * 70)
        sys.exit(0)

    process_show(args.show, force=args.force, send_email=not args.no_email)

if __name__ == '__main__':
    main()
