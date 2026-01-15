"""
YouTube playlist and transcript handling module using yt-dlp.
"""
import os
import json
from datetime import datetime
from typing import Optional, Dict
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


class YouTubeHandler:
    """Handles YouTube playlist and transcript operations."""

    def __init__(self, playlist_id: str, api_key: Optional[str] = None):
        """
        Initialize YouTube handler.

        Args:
            playlist_id: YouTube playlist ID
            api_key: Optional YouTube Data API key (not used with yt-dlp, kept for compatibility)
        """
        self.playlist_id = playlist_id
        self.api_key = api_key

    def get_latest_video_id(self) -> Optional[str]:
        """
        Get the video ID of the latest video in the playlist.
        Uses YouTube API if available, falls back to yt-dlp.

        Returns:
            Video ID or None if unable to fetch
        """
        # Try YouTube API first if available
        if self.api_key:
            try:
                from googleapiclient.discovery import build
                print(f"Fetching latest video from playlist using YouTube API...")

                youtube = build('youtube', 'v3', developerKey=self.api_key)
                request = youtube.playlistItems().list(
                    part='snippet',
                    playlistId=self.playlist_id,
                    maxResults=1
                )
                response = request.execute()

                if 'items' in response and response['items']:
                    video_id = response['items'][0]['snippet']['resourceId']['videoId']
                    video_title = response['items'][0]['snippet']['title']
                    print(f"Found latest video: {video_title} ({video_id})")
                    return video_id
                else:
                    print("No videos found in playlist")
                    return None

            except ImportError:
                print("google-api-python-client not installed, falling back to yt-dlp")
                print("Install with: pip install google-api-python-client")
            except Exception as e:
                print(f"Error with YouTube API: {e}")
                print("Falling back to yt-dlp...")

        # Fallback to yt-dlp
        playlist_url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Don't download, just get metadata
            'playlist_items': '1',  # Only get the first (latest) video
        }

        try:
            print(f"Fetching latest video from playlist (no API key)...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)

                if 'entries' not in info or not info['entries']:
                    print("No videos found in playlist")
                    return None

                # Get the first video entry
                first_entry = info['entries'][0]
                video_id = first_entry.get('id')
                video_title = first_entry.get('title', 'Unknown')

                if video_id:
                    print(f"Found latest video: {video_title} ({video_id})")
                    return video_id
                else:
                    print("Could not extract video ID from playlist")
                    return None

        except Exception as e:
            print(f"Error fetching playlist with yt-dlp: {e}")
            return None

    def get_transcript(self, video_id: str) -> Optional[Dict]:
        """
        Get transcript for a video. Tries multiple methods in order of reliability.

        Args:
            video_id: YouTube video ID

        Returns:
            Dictionary with transcript text and metadata, or None if unavailable
        """
        # Try Method 1: youtube-transcript-api (fastest, no API quota)
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Try to get manual transcript first (more accurate)
            try:
                transcript = transcript_list.find_manually_created_transcript(['en'])
            except:
                # Fall back to auto-generated
                transcript = transcript_list.find_generated_transcript(['en'])

            # Fetch the actual transcript
            transcript_data = transcript.fetch()

            # Combine all text segments
            full_text = ' '.join([entry['text'] for entry in transcript_data])

            print(f"Transcript extracted via youtube-transcript-api: {len(full_text)} characters")
            return {
                'video_id': video_id,
                'text': full_text,
                'language': transcript.language_code,
                'is_generated': transcript.is_generated,
                'fetched_at': datetime.now().isoformat(),
                'method': 'youtube-transcript-api'
            }

        except Exception as e:
            print(f"youtube-transcript-api failed: {e}")

        # Try Method 2: yt-dlp subtitle extraction (bypasses some bot detection)
        try:
            print("Trying yt-dlp subtitle extraction...")
            return self._get_transcript_with_ytdlp(video_id)
        except Exception as e:
            print(f"yt-dlp subtitle extraction also failed: {e}")
            return None

    def _get_transcript_with_ytdlp(self, video_id: str) -> Optional[Dict]:
        """
        Extract transcript using yt-dlp auto-generated subtitles.

        Args:
            video_id: YouTube video ID

        Returns:
            Dictionary with transcript text and metadata
        """
        import subprocess
        from pathlib import Path

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        temp_dir = Path('temp')
        temp_dir.mkdir(exist_ok=True)

        try:
            # Use yt-dlp to download auto-generated captions
            cmd = [
                'yt-dlp',
                '--write-auto-subs',
                '--sub-lang', 'en',
                '--skip-download',
                '--sub-format', 'json3',
                '--extractor-args', 'youtube:player_client=android',  # Use Android client to avoid bot detection
                '-o', f'temp/{video_id}',
                video_url
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Find the subtitle file
            subtitle_file = temp_dir / f'{video_id}.en.json3'
            if not subtitle_file.exists():
                raise FileNotFoundError(f"Subtitle file not found: {subtitle_file}")

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

            full_text = ' '.join(transcript_parts)

            # Clean up subtitle file
            subtitle_file.unlink()

            print(f"Transcript extracted via yt-dlp: {len(full_text)} characters")

            return {
                'video_id': video_id,
                'text': full_text,
                'language': 'en',
                'is_generated': True,
                'fetched_at': datetime.now().isoformat(),
                'method': 'yt-dlp'
            }

        except subprocess.CalledProcessError as e:
            raise Exception(f"yt-dlp command failed: {e.stderr}")
        except Exception as e:
            raise Exception(f"Subtitle extraction error: {str(e)}")

    def get_video_metadata(self, video_id: str) -> Optional[Dict]:
        """
        Get video metadata using yt-dlp.

        Args:
            video_id: YouTube video ID

        Returns:
            Dictionary with video metadata or None if unavailable
        """
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)

                return {
                    'video_id': video_id,
                    'title': info.get('title', 'Unknown'),
                    'description': info.get('description', ''),
                    'published_at': info.get('upload_date', ''),
                    'channel_title': info.get('uploader', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'url': video_url
                }
        except Exception as e:
            print(f"Error fetching video metadata: {e}")
            # Return basic info at minimum
            return {
                'video_id': video_id,
                'url': video_url
            }

    def save_transcript(self, transcript_data: Dict, output_dir: str = 'transcripts'):
        """
        Save transcript to a JSON file.

        Args:
            transcript_data: Transcript data dictionary
            output_dir: Directory to save transcripts
        """
        os.makedirs(output_dir, exist_ok=True)

        video_id = transcript_data['video_id']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/{video_id}_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(transcript_data, f, indent=2, ensure_ascii=False)

        print(f"Transcript saved to {filename}")
        return filename
