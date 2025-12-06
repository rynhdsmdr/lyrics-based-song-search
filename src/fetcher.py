import requests
import time
import re

GENIUS_TOKEN="fQKrqH_9EoK5weRkHquwftHirsEPf3UVWvE2nP4CcxxZx6iCBsjuXA5FN1BvAFlf"


# =======================
# CLEAN TEXT
# =======================
def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)  # Hapus newline/tab/multispaces
    return text.strip()


# =======================
# SEARCH ARTIST ID
# =======================
def search_artist_on_genius(name):
    url = "https://api.genius.com/search"
    params = {"q": name}
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}

    for _ in range(3):  # Retry 3 kali
        try:
            res = requests.get(url, params=params, headers=headers, timeout=15)
            if res.status_code != 200:
                continue

            hits = res.json()["response"]["hits"]
            if not hits:
                return None

            return hits[0]["result"]["primary_artist"]["id"]

        except requests.exceptions.Timeout:
            print("⏳ Timeout saat mencari artist... retrying")
            time.sleep(1)

    return None


# =======================
# GET SONG LIST
# =======================
def get_songs_by_artist(artist_id, limit=50):
    url = f"https://api.genius.com/artists/{artist_id}/songs"
    params = {"per_page": limit, "sort": "popularity"}
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}

    try:
        res = requests.get(url, params=params, headers=headers, timeout=15)
        if res.status_code != 200:
            return []
        songs = res.json()["response"]["songs"]
        return [{"title": s["title"], "url": s["url"]} for s in songs]
    except:
        return []


# =======================
# FETCH LYRICS
# =======================
def fetch_lyrics(title, artist):
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"

    for _ in range(3):
        try:
            res = requests.get(url, timeout=20)
            if res.status_code != 200:
                return None

            lyrics = res.json().get("lyrics", "")
            return clean_text(lyrics)

        except:
            print("⚠️ Error fetching lyrics... retrying")
            time.sleep(1)

    return None


# =======================
# MAIN FETCH FUNCTION
# =======================
def crawl_artist(artist_name, writer):
    print(f"\n====================")
    print(f"🎤 ARTIST: {artist_name}")
    print(f"====================")

    # Cari artist ID dari Genius
    artist_id = search_artist_on_genius(artist_name)
    if not artist_id:
        print(f"❌ Artist '{artist_name}' tidak ditemukan")
        return 0

    print(f"🎯 Artist ID = {artist_id}")

    songs = get_songs_by_artist(artist_id, limit=50)
    saved = 0

    for song in songs:
        print(f"   🎶 Fetching: {song['title']}")

        lyrics = fetch_lyrics(song["title"], artist_name)
        if lyrics:
            writer.writerow([
                artist_name,
                clean_text(song["title"]),
                lyrics,
                song["url"]
            ])
            saved += 1

        time.sleep(1.5)  # anti rate limit

    return saved
