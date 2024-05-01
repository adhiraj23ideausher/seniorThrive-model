from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
load_dotenv()
import os

api_key=os.getenv("YOUTUBE_API_KEY")

def search_videos(query, max_results=5):
    youtube = build('youtube', 'v3', developerKey=api_key)
    search_params = {
        'q': query,
        'part': 'id,snippet',
        'maxResults': max_results
    }
    
    search_params['channelId'] = 'UCqd2hbtE2N9fb0D2nTrLT1w'

    search_response = youtube.search().list(**search_params).execute()

    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            videos.append(video_url)
    return videos

