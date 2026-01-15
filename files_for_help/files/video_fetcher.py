"""
Video fetcher module for Bloomberg Markets videos
"""

import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
import yt_dlp


class VideoFetcher:
    """Fetches and downloads Bloomberg Markets videos"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.video_config = config['video']
    
    def get_latest_video(self):
        """
        Find the latest Bloomberg Markets video
        Returns dict with video info or None
        """
        source_url = self.video_config['source_url']
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.logger.info(f"Fetching videos from: {source_url}")
                info = ydl.extract_info(source_url, download=False)
                
                if 'entries' not in info:
                    self.logger.error("No videos found in channel")
                    return None
                
                # Filter videos by keywords and age
                max_age = timedelta(hours=self.video_config.get('max_age_hours', 24))
                keywords = self.video_config.get('title_keywords', ['Bloomberg Markets'])
                
                for entry in info['entries']:
                    title = entry.get('title', '')
                    
                    # Check if title matches keywords
                    if not any(keyword.lower() in title.lower() for keyword in keywords):
                        continue
                    
                    # Check video age
                    upload_date_str = entry.get('upload_date')
                    if upload_date_str:
                        upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
                        if datetime.now() - upload_date > max_age:
                            continue
                    
                    # Found a matching video
                    video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                    
                    return {
                        'title': title,
                        'url': video_url,
                        'id': entry['id'],
                        'upload_date': upload_date_str,
                        'duration': entry.get('duration'),
                    }
                
                self.logger.warning("No videos matched criteria")
                return None
                
        except Exception as e:
            self.logger.error(f"Error fetching videos: {str(e)}")
            raise
    
    def download_audio(self, video_url):
        """
        Download video and extract audio
        Returns path to audio file
        """
        output_dir = Path('temp')
        output_dir.mkdir(exist_ok=True)
        
        output_template = str(output_dir / 'bloomberg_audio')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'no_warnings': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.logger.info(f"Downloading audio from: {video_url}")
                ydl.download([video_url])
            
            # Find the downloaded file
            audio_files = list(output_dir.glob('bloomberg_audio*.mp3'))
            if not audio_files:
                raise FileNotFoundError("Audio file not found after download")
            
            audio_path = audio_files[0]
            self.logger.info(f"Audio downloaded: {audio_path}")
            
            return str(audio_path)
            
        except Exception as e:
            self.logger.error(f"Error downloading audio: {str(e)}")
            raise
