#!/usr/bin/env python3
"""
Helper script to find YouTube playlist IDs for Bloomberg shows.
"""
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def search_youtube_playlists(query: str, api_key: str):
    """Search for playlists matching a query."""
    try:
        from googleapiclient.discovery import build
    except ImportError:
        print("Error: google-api-python-client not installed")
        print("Install with: pip install google-api-python-client")
        sys.exit(1)

    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        # Search for playlists
        request = youtube.search().list(
            part='snippet',
            q=query,
            type='playlist',
            maxResults=10
        )
        response = request.execute()

        if not response.get('items'):
            print(f"No playlists found for: {query}")
            return

        print(f"\nFound {len(response['items'])} playlists for '{query}':\n")
        print("-" * 100)

        for i, item in enumerate(response['items'], 1):
            playlist_id = item['id']['playlistId']
            title = item['snippet']['title']
            channel = item['snippet']['channelTitle']
            description = item['snippet']['description'][:100]

            print(f"{i}. {title}")
            print(f"   Channel: {channel}")
            print(f"   Playlist ID: {playlist_id}")
            print(f"   Description: {description}...")
            print(f"   URL: https://www.youtube.com/playlist?list={playlist_id}")
            print("-" * 100)

    except Exception as e:
        print(f"Error searching YouTube: {e}")
        sys.exit(1)

def main():
    load_dotenv()

    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("Error: YOUTUBE_API_KEY not found in .env file")
        sys.exit(1)

    # Common Bloomberg shows
    bloomberg_shows = [
        "Bloomberg Surveillance",
        "Bloomberg Markets",
        "Bloomberg Technology",
        "Bloomberg Wall Street Week",
        "Bloomberg The Open",
        "Bloomberg Brief"
    ]

    print("=" * 100)
    print("Bloomberg Playlist Finder")
    print("=" * 100)

    if len(sys.argv) > 1:
        # Search for specific show
        query = ' '.join(sys.argv[1:])
        search_youtube_playlists(query, api_key)
    else:
        # Show menu
        print("\nCommon Bloomberg Shows:")
        for i, show in enumerate(bloomberg_shows, 1):
            print(f"{i}. {show}")

        print(f"{len(bloomberg_shows) + 1}. Custom search")
        print()

        try:
            choice = input("Select a show to search (or press Enter to exit): ").strip()

            if not choice:
                sys.exit(0)

            choice_num = int(choice)

            if 1 <= choice_num <= len(bloomberg_shows):
                query = bloomberg_shows[choice_num - 1]
            elif choice_num == len(bloomberg_shows) + 1:
                query = input("Enter search query: ").strip()
            else:
                print("Invalid choice")
                sys.exit(1)

            search_youtube_playlists(query, api_key)

        except ValueError:
            print("Invalid input")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

if __name__ == '__main__':
    main()
