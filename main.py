#!/usr/bin/env python3
"""
The Great Information Gatherer - Main Script

Fetches the latest video from a YouTube playlist, extracts the transcript,
generates a macro trading-focused summary, and emails it to specified recipients.
"""
import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from youtube_handler import YouTubeHandler
try:
    from summarizer_v2 import MacroTradingSummarizer
    from output_manager import OutputManager
    USE_V2 = True
except ImportError:
    from summarizer import MacroTradingSummarizer
    USE_V2 = False
    print("Note: Using legacy summarizer. Install pyyaml for config support.")
from email_sender import EmailSender


def load_config():
    """Load configuration from environment variables."""
    load_dotenv()

    config = {
        'playlist_id': os.getenv('YOUTUBE_PLAYLIST_ID'),
        'youtube_api_key': os.getenv('YOUTUBE_API_KEY'),
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
        'smtp_server': os.getenv('SMTP_SERVER'),
        'smtp_port': int(os.getenv('SMTP_PORT', 587)),
        'smtp_username': os.getenv('SMTP_USERNAME'),
        'smtp_password': os.getenv('SMTP_PASSWORD'),
        'email_from': os.getenv('EMAIL_FROM'),
        'email_to': os.getenv('EMAIL_TO'),
    }

    # Validate required config
    required = ['playlist_id', 'anthropic_api_key', 'email_to']
    missing = [key for key in required if not config.get(key)]

    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        print("Please check your .env file or environment configuration.")
        sys.exit(1)

    return config


def save_summary_to_file(summary_data: dict, markdown_content: str = None, output_dir: str = 'summaries'):
    """
    Save summary to files (JSON and/or Markdown).

    Args:
        summary_data: Summary data dictionary
        markdown_content: Optional markdown formatted summary
        output_dir: Directory to save summaries (legacy parameter)
    """
    if USE_V2:
        # Use new output manager with date-based folders
        output_manager = OutputManager()
        saved_files = output_manager.save_summary(summary_data, markdown_content)
        return saved_files
    else:
        # Legacy flat structure
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_id = summary_data.get('video_metadata', {}).get('video_id', 'unknown')
        filename = f"{output_dir}/summary_{video_id}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        print(f"Summary saved to {filename}")
        return {'json': filename}


def check_if_already_processed(video_id: str, state_file: str = '.last_processed_video') -> bool:
    """
    Check if a video has already been processed.

    Args:
        video_id: YouTube video ID
        state_file: Path to state file

    Returns:
        True if already processed, False otherwise
    """
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            last_video_id = f.read().strip()
            return last_video_id == video_id
    return False


def mark_as_processed(video_id: str, state_file: str = '.last_processed_video'):
    """
    Mark a video as processed.

    Args:
        video_id: YouTube video ID
        state_file: Path to state file
    """
    with open(state_file, 'w') as f:
        f.write(video_id)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Generate and email macro trading summaries of YouTube videos'
    )
    parser.add_argument(
        '--video-id',
        help='Specific video ID to process (skips playlist lookup)'
    )
    parser.add_argument(
        '--no-email',
        action='store_true',
        help='Skip sending email (just generate and save summary)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force processing even if video was already processed'
    )
    parser.add_argument(
        '--test-email',
        action='store_true',
        help='Test email configuration and exit'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("The Great Information Gatherer - Macro Trading Video Summarizer")
    print("=" * 70)
    print()

    # Load configuration
    config = load_config()

    # Test email configuration if requested
    if args.test_email:
        print("Testing email configuration...")
        if not all([config['smtp_server'], config['smtp_username'], config['smtp_password']]):
            print("Error: Email configuration incomplete. Check SMTP settings in .env")
            sys.exit(1)

        sender = EmailSender(
            smtp_server=config['smtp_server'],
            smtp_port=config['smtp_port'],
            username=config['smtp_username'],
            password=config['smtp_password'],
            from_address=config['email_from']
        )
        success = sender.test_connection()
        sys.exit(0 if success else 1)

    # Initialize handlers
    yt_handler = YouTubeHandler(
        playlist_id=config['playlist_id'],
        api_key=config['youtube_api_key']
    )

    # Get video ID
    if args.video_id:
        video_id = args.video_id
        print(f"Using specified video ID: {video_id}")
    else:
        print(f"Fetching latest video from playlist: {config['playlist_id']}")
        video_id = yt_handler.get_latest_video_id()

        if not video_id:
            print("Error: Could not fetch latest video ID.")
            print("\nTroubleshooting:")
            print("1. Set YOUTUBE_API_KEY in your .env file for reliable playlist access")
            print("2. Or use --video-id flag to specify a video directly")
            sys.exit(1)

    # Check if already processed
    if not args.force and check_if_already_processed(video_id):
        print(f"Video {video_id} has already been processed.")
        print("Use --force to process again.")
        sys.exit(0)

    # Get video metadata
    print(f"\nFetching metadata for video: {video_id}")
    metadata = yt_handler.get_video_metadata(video_id)
    if metadata:
        print(f"Title: {metadata.get('title', 'N/A')}")
        print(f"Channel: {metadata.get('channel_title', 'N/A')}")

    # Get transcript
    print("\nExtracting transcript...")
    transcript_data = yt_handler.get_transcript(video_id)

    if not transcript_data:
        print("Error: Could not extract transcript. Video may not have captions available.")
        sys.exit(1)

    print(f"Transcript extracted successfully ({len(transcript_data['text'])} characters)")
    print(f"Language: {transcript_data['language']}")
    print(f"Auto-generated: {transcript_data['is_generated']}")

    # Save transcript
    yt_handler.save_transcript(transcript_data)

    # Generate summary
    print("\nGenerating macro trading summary with Claude...")
    if USE_V2:
        print("Using configurable summarizer (config.yaml)")
    summarizer = MacroTradingSummarizer(api_key=config['anthropic_api_key'])

    try:
        summary_data = summarizer.generate_summary(
            transcript=transcript_data['text'],
            video_metadata=metadata
        )
        print("✓ Summary generated successfully!")
        print(f"Tokens used: {summary_data['tokens_used']['input']} input, "
              f"{summary_data['tokens_used']['output']} output")

    except Exception as e:
        print(f"Error generating summary: {e}")
        sys.exit(1)

    # Generate markdown version
    markdown_content = None
    if USE_V2:
        markdown_content = summarizer.format_as_markdown(summary_data)

    # Save summary
    print("\nSaving summary files...")
    saved_files = save_summary_to_file(summary_data, markdown_content)
    if 'markdown' in saved_files:
        print(f"✓ Markdown available at: {saved_files['markdown']}")

    # Send email
    if not args.no_email:
        if not all([config['smtp_server'], config['smtp_username'], config['smtp_password']]):
            print("\nWarning: Email configuration incomplete. Skipping email send.")
            print("Set SMTP_* variables in .env to enable email delivery.")
        else:
            print("\nSending email...")
            sender = EmailSender(
                smtp_server=config['smtp_server'],
                smtp_port=config['smtp_port'],
                username=config['smtp_username'],
                password=config['smtp_password'],
                from_address=config['email_from']
            )

            email_html = summarizer.format_email_body(summary_data)
            video_title = metadata.get('title', 'Unknown Video') if metadata else 'Unknown Video'

            success = sender.send_summary_with_video_data(
                to_address=config['email_to'],
                summary_html=email_html,
                video_title=video_title,
                plain_text_summary=summary_data['summary']
            )

            if success:
                print("✓ Email sent successfully!")
            else:
                print("✗ Failed to send email. Check your SMTP configuration.")
                sys.exit(1)
    else:
        print("\nEmail sending skipped (--no-email flag)")

    # Mark as processed
    mark_as_processed(video_id)

    print("\n" + "=" * 70)
    print("Summary generation complete!")
    print("=" * 70)


if __name__ == '__main__':
    main()
