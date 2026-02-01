#!/usr/bin/env python3
"""
Process multiple Bloomberg shows and generate summaries.
Configure your shows in the SHOWS dictionary below.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from youtube_handler import YouTubeHandler
from summarizer_v2 import MacroTradingSummarizer
from output_manager import OutputManager
from email_sender import EmailSender

# Configure your Bloomberg shows here
SHOWS = {
    'Bloomberg Brief': {
        'playlist_id': 'PLGaYlBJIOoa_vIH-o9MQZHg86xdx496BW',
        'state_file': '.last_processed_bloomberg_brief'
    },
    # Add more shows here, for example:
    # 'Bloomberg Surveillance': {
    #     'playlist_id': 'YOUR_PLAYLIST_ID_HERE',
    #     'state_file': '.last_processed_surveillance'
    # },
    # 'Bloomberg Markets': {
    #     'playlist_id': 'YOUR_PLAYLIST_ID_HERE',
    #     'state_file': '.last_processed_markets'
    # },
}

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

def process_show(show_name: str, config: dict, force: bool = False) -> dict:
    """
    Process a single show.

    Returns:
        dict with keys: success, video_id, title, summary_files, error
    """
    print(f"\n{'='*70}")
    print(f"Processing: {show_name}")
    print(f"{'='*70}")

    # Load environment
    load_dotenv()

    # Initialize handlers
    yt_handler = YouTubeHandler(
        playlist_id=config['playlist_id'],
        api_key=os.getenv('YOUTUBE_API_KEY')
    )

    # Get latest video
    print(f"Fetching latest video from playlist...")
    video_id = yt_handler.get_latest_video_id()

    if not video_id:
        return {
            'success': False,
            'show': show_name,
            'error': 'Could not fetch latest video ID'
        }

    # Check if already processed
    if not force and check_if_processed(video_id, config['state_file']):
        print(f"✓ Video {video_id} already processed. Skipping.")
        return {
            'success': True,
            'show': show_name,
            'video_id': video_id,
            'skipped': True
        }

    # Get metadata and transcript
    print(f"Fetching metadata for: {video_id}")
    metadata = yt_handler.get_video_metadata(video_id)

    if metadata:
        print(f"Title: {metadata.get('title', 'N/A')}")

    print("Extracting transcript...")
    transcript_data = yt_handler.get_transcript(video_id)

    if not transcript_data:
        return {
            'success': False,
            'show': show_name,
            'video_id': video_id,
            'error': 'Could not extract transcript'
        }

    print(f"✓ Transcript extracted ({len(transcript_data['text'])} chars)")

    # Save transcript
    yt_handler.save_transcript(transcript_data)

    # Generate summary
    print("Generating summary with Claude...")
    summarizer = MacroTradingSummarizer(api_key=os.getenv('ANTHROPIC_API_KEY'))

    try:
        summary_data = summarizer.generate_summary(
            transcript=transcript_data['text'],
            video_metadata=metadata
        )
        print(f"✓ Summary generated!")
        print(f"  Tokens: {summary_data['tokens_used']['input']} input, "
              f"{summary_data['tokens_used']['output']} output")

    except Exception as e:
        return {
            'success': False,
            'show': show_name,
            'video_id': video_id,
            'error': f'Summary generation failed: {e}'
        }

    # Save summary
    markdown_content = summarizer.format_as_markdown(summary_data)
    output_manager = OutputManager()
    saved_files = output_manager.save_summary(summary_data, markdown_content)

    print(f"✓ Saved to: {saved_files.get('markdown', saved_files.get('json'))}")

    # Mark as processed
    mark_as_processed(video_id, config['state_file'])

    return {
        'success': True,
        'show': show_name,
        'video_id': video_id,
        'title': metadata.get('title', 'N/A') if metadata else 'N/A',
        'summary_files': saved_files,
        'summary_data': summary_data,
        'metadata': metadata
    }

def send_combined_email(results: list):
    """Send a single email with all summaries."""
    load_dotenv()

    # Check if email is configured
    if not all([os.getenv('SMTP_SERVER'), os.getenv('SMTP_USERNAME'),
                os.getenv('SMTP_PASSWORD'), os.getenv('EMAIL_TO')]):
        print("\n⚠️  Email not configured. Skipping email send.")
        return False

    sender = EmailSender(
        smtp_server=os.getenv('SMTP_SERVER'),
        smtp_port=int(os.getenv('SMTP_PORT', 587)),
        username=os.getenv('SMTP_USERNAME'),
        password=os.getenv('SMTP_PASSWORD'),
        from_address=os.getenv('EMAIL_FROM')
    )

    # Build combined email
    summarizer = MacroTradingSummarizer(api_key=os.getenv('ANTHROPIC_API_KEY'))

    email_parts = []
    for result in results:
        if result.get('success') and not result.get('skipped'):
            email_html = summarizer.format_email_body(result['summary_data'])
            email_parts.append(email_html)

    if not email_parts:
        print("No new summaries to email.")
        return False

    # Combine all summaries
    combined_html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .show-divider { margin: 40px 0; border-top: 3px solid #3498db; }
        </style>
    </head>
    <body>
    """ + '<div class="show-divider"></div>'.join(email_parts) + """
    </body>
    </html>
    """

    # Send email
    subject = f"📊 Daily Bloomberg Summaries ({len(email_parts)} shows)"
    success = sender.send_email(
        to_address=os.getenv('EMAIL_TO'),
        subject=subject,
        html_body=combined_html,
        plain_text_body=f"{len(email_parts)} new Bloomberg show summaries available."
    )

    if success:
        print(f"✓ Email sent with {len(email_parts)} summaries!")
    else:
        print("✗ Failed to send email.")

    return success

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Process multiple Bloomberg shows and generate summaries'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force reprocessing of already-processed videos'
    )
    parser.add_argument(
        '--no-email',
        action='store_true',
        help='Skip sending email'
    )
    parser.add_argument(
        '--show',
        help='Process only this specific show name'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("Multi-Show Bloomberg Summarizer")
    print("=" * 70)

    # Filter shows if specific one requested
    shows_to_process = SHOWS
    if args.show:
        if args.show in SHOWS:
            shows_to_process = {args.show: SHOWS[args.show]}
        else:
            print(f"Error: Show '{args.show}' not found in configuration.")
            print(f"Available shows: {', '.join(SHOWS.keys())}")
            sys.exit(1)

    # Process all shows
    results = []
    for show_name, show_config in shows_to_process.items():
        result = process_show(show_name, show_config, force=args.force)
        results.append(result)

    # Print summary
    print("\n" + "=" * 70)
    print("PROCESSING SUMMARY")
    print("=" * 70)

    for result in results:
        status = "✓" if result['success'] else "✗"
        show = result['show']

        if result.get('skipped'):
            print(f"{status} {show}: Already processed")
        elif result['success']:
            print(f"{status} {show}: {result['title'][:60]}...")
        else:
            print(f"{status} {show}: {result.get('error', 'Unknown error')}")

    # Send email if requested
    if not args.no_email:
        print("\n" + "=" * 70)
        print("SENDING EMAIL")
        print("=" * 70)
        send_combined_email(results)

    print("\n" + "=" * 70)
    print("Complete!")
    print("=" * 70)

if __name__ == '__main__':
    main()
