"""
Free transcript extractor using YouTube's auto-generated captions
NO API KEYS NEEDED!
"""

import logging
import subprocess
import json
from pathlib import Path


class FreeTranscriber:
    """Extract transcripts from YouTube using free auto-captions"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def get_transcript(self, video_url):
        """
        Extract YouTube auto-generated captions (FREE!)
        Returns transcript text
        """
        self.logger.info(f"Extracting free transcript from YouTube: {video_url}")
        
        try:
            # Use yt-dlp to download subtitles without downloading video
            cmd = [
                'yt-dlp',
                '--write-auto-subs',  # Get auto-generated captions
                '--sub-lang', 'en',    # English captions
                '--skip-download',     # Don't download video
                '--sub-format', 'json3',  # JSON format for easy parsing
                '-o', 'temp/%(id)s',   # Output location
                video_url
            ]
            
            self.logger.info("Downloading YouTube auto-captions (FREE)...")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Find the downloaded subtitle file
            subtitle_files = list(Path('temp').glob('*.en.json3'))
            if not subtitle_files:
                raise FileNotFoundError("No subtitle file found")
            
            subtitle_file = subtitle_files[0]
            self.logger.info(f"Found subtitle file: {subtitle_file}")
            
            # Parse JSON subtitle file
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                subtitle_data = json.load(f)
            
            # Extract text from subtitles
            transcript_parts = []
            
            if 'events' in subtitle_data:
                for event in subtitle_data['events']:
                    if 'segs' in event:
                        for seg in event['segs']:
                            if 'utf8' in seg:
                                text = seg['utf8'].strip()
                                if text and text != '\n':
                                    transcript_parts.append(text)
            
            transcript = ' '.join(transcript_parts)
            
            # Clean up subtitle file
            subtitle_file.unlink()
            
            self.logger.info(f"FREE transcript extracted: {len(transcript)} characters")
            return transcript
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error extracting captions: {e.stderr}")
            raise Exception("Could not extract YouTube captions. Video may not have auto-captions enabled.")
        except Exception as e:
            self.logger.error(f"Transcript extraction error: {str(e)}")
            raise


def test_free_transcript():
    """Test the free transcript extraction"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python free_transcriber.py <youtube_url>")
        sys.exit(1)
    
    # Setup basic config
    config = {}
    
    # Test extraction
    transcriber = FreeTranscriber(config)
    transcript = transcriber.get_transcript(sys.argv[1])
    
    print(f"\n{'='*60}")
    print("FREE TRANSCRIPT EXTRACTED!")
    print(f"{'='*60}")
    print(f"Length: {len(transcript)} characters")
    print(f"\nFirst 500 characters:")
    print(transcript[:500])
    print(f"{'='*60}\n")


if __name__ == "__main__":
    test_free_transcript()
