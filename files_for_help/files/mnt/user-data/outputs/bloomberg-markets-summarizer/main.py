#!/usr/bin/env python3
"""
Bloomberg Markets Daily Summarizer
Main orchestration script
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import yaml

from src.video_fetcher import VideoFetcher
from src.transcriber import Transcriber
from src.free_transcriber import FreeTranscriber
from src.summarizer import Summarizer
from src.utils import setup_logging, ensure_directories

# Load environment variables
load_dotenv()

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


def main():
    """Main execution flow"""
    
    # Setup
    logger = setup_logging(config)
    ensure_directories(config)
    
    logger.info("="*60)
    logger.info("Bloomberg Markets Summarizer - Starting")
    logger.info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*60)
    
    try:
        # Step 1: Fetch video
        logger.info("Step 1: Fetching latest Bloomberg Markets video...")
        fetcher = VideoFetcher(config)
        video_info = fetcher.get_latest_video()
        
        if not video_info:
            logger.error("No suitable video found")
            return 1
        
        logger.info(f"Found video: {video_info['title']}")
        logger.info(f"URL: {video_info['url']}")
        
        # Step 2: Download and extract audio
        logger.info("Step 2: Downloading video and extracting audio...")
        audio_path = fetcher.download_audio(video_info['url'])
        logger.info(f"Audio saved to: {audio_path}")
        
        # Step 3: Transcribe
        logger.info("Step 3: Transcribing audio...")
        
        # Check if we should use FREE YouTube captions or paid transcription
        use_free = config['transcription'].get('use_free_youtube_captions', True)
        
        if use_free:
            logger.info("Using FREE YouTube auto-captions (no API key needed!)")
            transcriber = FreeTranscriber(config)
            transcript = transcriber.get_transcript(video_info['url'])
        else:
            logger.info("Using paid transcription service")
            transcriber = Transcriber(config)
            transcript = transcriber.transcribe(audio_path)
        
        # Save transcript
        today = datetime.now().strftime('%Y-%m-%d')
        transcript_path = Path(config['output']['directory']) / 'transcripts' / f'{today}_transcript.txt'
        transcript_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        logger.info(f"Transcript saved to: {transcript_path}")
        logger.info(f"Transcript length: {len(transcript)} characters")
        
        # Step 4: Generate summary
        logger.info("Step 4: Generating AI summary...")
        summarizer = Summarizer(config)
        summary = summarizer.summarize(transcript, video_info)
        
        # Save summary
        summary_path = Path(config['output']['directory']) / 'summaries' / f'{today}_summary.md'
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        # Create/update latest summary symlink
        latest_path = Path(config['output']['directory']) / 'latest_summary.md'
        if latest_path.exists():
            latest_path.unlink()
        
        # Write content instead of symlink for compatibility
        with open(latest_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        logger.info(f"Summary saved to: {summary_path}")
        logger.info(f"Latest summary: {latest_path}")
        
        # Step 5: Cleanup old files (if configured)
        if config['output'].get('archive', True):
            archive_days = config['output'].get('archive_days', 90)
            logger.info(f"Cleaning up files older than {archive_days} days...")
            cleanup_old_files(config, archive_days)
        
        # Step 6: Send notifications (if enabled)
        if config['notifications'].get('enabled', False):
            logger.info("Sending notifications...")
            send_notifications(config, summary_path, success=True)
        
        logger.info("="*60)
        logger.info("Bloomberg Markets Summarizer - Completed Successfully")
        logger.info("="*60)
        
        return 0
        
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}", exc_info=True)
        
        # Send error notification
        if config['notifications'].get('enabled', False) and config['notifications'].get('on_error', True):
            send_notifications(config, None, success=False, error=str(e))
        
        return 1


def cleanup_old_files(config, days):
    """Remove files older than specified days"""
    from datetime import timedelta
    
    cutoff_date = datetime.now() - timedelta(days=days)
    output_dir = Path(config['output']['directory'])
    
    for subdir in ['summaries', 'transcripts']:
        dir_path = output_dir / subdir
        if not dir_path.exists():
            continue
            
        for file in dir_path.glob('*'):
            if file.is_file():
                file_date_str = file.stem.split('_')[0]
                try:
                    file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
                    if file_date < cutoff_date:
                        file.unlink()
                        logging.info(f"Deleted old file: {file}")
                except ValueError:
                    pass


def send_notifications(config, summary_path, success=True, error=None):
    """Send notifications based on configuration"""
    # Placeholder for notification implementation
    # Can add email, Slack, Telegram, etc.
    pass


if __name__ == "__main__":
    sys.exit(main())
