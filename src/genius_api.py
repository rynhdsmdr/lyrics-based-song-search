import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GENIUS_TOKEN")
BASE_URL = "https://api.genius.com"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# 1) Ambil data artis
def search_artist(name):
    url = f"{BASE_URL}/search?q={name}"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return None
    
    hits = r.json()["response"]["hits"]
    for h in hits:
        if h["type"] == "artist":
            return h["result"]["id"]
    return None


# 2) Ambil daftar lagu artis
def get_artist_songs(artist_id, limit=10):
    url = f"{BASE_URL}/artists/{artist_id}/songs?sort=popularity"
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return []

    songs = r.json()["response"]["songs"]
    data = []

    for s in songs[:limit]:
        data.append({
            "title": s["full_title"],
            "url": s["url"]
        })

    return data
