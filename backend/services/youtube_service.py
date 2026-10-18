import os
import requests
from dotenv import load_dotenv

load_dotenv()


def search_youtube(query: str, limit: int = 10):

    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise ValueError("YOUTUBE_API_KEY is not configured")

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": limit,
        "key": api_key
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get("items", []):
        results.append({
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            "channel": item["snippet"]["channelTitle"],
            "source": "YouTube"
        })

    return results