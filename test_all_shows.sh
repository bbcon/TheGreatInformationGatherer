#!/bin/bash
# Test script to verify all shows can fetch their latest video
# This doesn't generate summaries, just checks connectivity

echo "========================================================================"
echo "Testing All Bloomberg Shows"
echo "========================================================================"
echo ""

SHOWS=("bloomberg_brief" "bloomberg_surveillance" "daybreak_europe" "the_china_show" "the_close")

for show in "${SHOWS[@]}"; do
    echo "Testing: $show"
    echo "------------------------------------------------------------------------"

    # Just check if we can fetch the latest video (no summary, no email)
    python3 -c "
import sys
import os
sys.path.insert(0, 'src')
from dotenv import load_dotenv
from youtube_handler import YouTubeHandler
import yaml

load_dotenv()

with open('shows_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

show_config = config['shows']['$show']
yt_handler = YouTubeHandler(
    playlist_id=show_config['playlist_id'],
    api_key=os.getenv('YOUTUBE_API_KEY')
)

video_id = yt_handler.get_latest_video_id()
if video_id:
    metadata = yt_handler.get_video_metadata(video_id)
    title = metadata.get('title', 'N/A') if metadata else 'N/A'
    print(f'✓ Latest video: {video_id}')
    print(f'  Title: {title[:70]}...')
else:
    print('✗ Could not fetch video')
    sys.exit(1)
"

    if [ $? -eq 0 ]; then
        echo "✓ Success"
    else
        echo "✗ Failed"
    fi
    echo ""
done

echo "========================================================================"
echo "Test Complete!"
echo "========================================================================"
