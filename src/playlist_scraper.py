"""
Fallback playlist scraper for when YouTube API is not available.
Uses web scraping to get the latest video from a playlist.
"""
import re
import json
from typing import Optional
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


def get_latest_video_from_playlist_url(playlist_id: str) -> Optional[dict]:
    """
    Scrape the playlist page to get the latest video ID.

    Args:
        playlist_id: YouTube playlist ID

    Returns:
        Dictionary with video_id and title, or None if failed
    """
    if not REQUESTS_AVAILABLE:
        print("Error: requests library not available")
        return None

    try:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        print(f"Fetching playlist page: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        html = response.text

        # Look for ytInitialData in the page
        # This contains the playlist information in JSON format
        match = re.search(r'var ytInitialData = ({.*?});', html)
        if not match:
            print("Could not find playlist data in page")
            return None

        data = json.loads(match.group(1))

        # Navigate through the nested structure to find videos
        try:
            contents = data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']

            # Get the first video (most recent)
            for item in contents:
                if 'playlistVideoRenderer' in item:
                    video = item['playlistVideoRenderer']
                    video_id = video['videoId']
                    title = video['title']['runs'][0]['text']

                    print(f"Found latest video: {title}")
                    return {
                        'video_id': video_id,
                        'title': title,
                        'url': f"https://www.youtube.com/watch?v={video_id}"
                    }
        except (KeyError, IndexError) as e:
            print(f"Could not parse playlist structure: {e}")

            # Try alternative structure (sometimes YouTube changes this)
            try:
                # Look for video IDs in the page with regex as backup
                video_ids = re.findall(r'"videoId":"([^"]+)"', html)
                if video_ids:
                    video_id = video_ids[0]
                    print(f"Found video ID via regex: {video_id}")
                    return {
                        'video_id': video_id,
                        'title': 'Unknown Title',
                        'url': f"https://www.youtube.com/watch?v={video_id}"
                    }
            except Exception as e2:
                print(f"Fallback method also failed: {e2}")

        return None

    except requests.RequestException as e:
        print(f"Error fetching playlist page: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
