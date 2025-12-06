import requests
import csv
import os
from bs4 import BeautifulSoup

GENIUS_TOKEN = "GENIUS_TOKEN"

HEADERS = {
    "Authorization": f"Bearer {GENIUS_TOKEN}"
}

# =========================================
# SEARCH ARTIST → ambil artist_id
# =========================================
def get_artist_id(artist_name):
    url = f"https://api.genius.com/search?q={artist_name}"
    r = requests.get(url, headers=HEADERS).json()

    hits = r["response"]["hits"]
    if not hits:
        print(f"[!] Artis '{artist_name}' tidak ditemukan.")
        return None

    for h in hits:
        if h["result"]["primary_artist"]["name"].lower() == artist_name.lower():
            return h["result"]["primary_artist"]["id"]

    print(f"[!] Tidak ada artist_id cocok untuk: {artist_name}")
    return None


# =========================================
# GET SONG LIST
# =========================================
def get_songs_from_artist(artist_id):
    songs = []
    page = 1

    while True:
        url = f"https://api.genius.com/artists/{artist_id}/songs?sort=popularity&per_page=50&page={page}"
        r = requests.get(url, headers=HEADERS).json()

        batch = r["response"]["songs"]
        if not batch:
            break

        songs.extend(batch)
        page += 1

    return songs


# =========================================
# SCRAPE LYRICS
# =========================================
def scrape_lyrics(genius_url):
    html = requests.get(genius_url).text
    soup = BeautifulSoup(html, "html.parser")

    blocks = soup.find_all("div", {"data-lyrics-container": "true"})
    if not blocks:
        return ""

    text_parts = [b.get_text(separator="\n") for b in blocks]
    return "\n".join(text_parts)


# =========================================
# SAVE TO CSV
# =========================================
def save_to_csv(data, filename="lyrics_dataset.csv"):
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # header kalau file belum ada
        if not file_exists:
            writer.writerow(["artist", "title", "lyrics", "image_url", "genius_url"])

        for row in data:
            writer.writerow(row)


# =========================================
# SCRAPE PER ARTIS
# =========================================
def scrape_genius_artist(artist_name):
    print(f"\n====== MULAI PROSES: {artist_name} ======")

    artist_id = get_artist_id(artist_name)
    if not artist_id:
        return

    print("[+] Mengambil daftar lagu...")
    songs = get_songs_from_artist(artist_id)

    print(f"[+] Total lagu ditemukan: {len(songs)}")

    rows = []

    for s in songs:
        title = s["title"]
        artist = s["primary_artist"]["name"]
        url = s["url"]
        image = s.get("song_art_image_url", "")

        print(f"[+] Scraping lirik: {title}")
        lyrics = scrape_lyrics(url)

        rows.append([artist, title, lyrics, image, url])

    save_to_csv(rows)
    print(f"[✓] Selesai untuk artis: {artist_name}\n")


# =========================================
# MAIN — SUPPORT MULTIPLE ARTISTS
# =========================================
artist_input = input("Masukkan daftar artis (pisahkan dengan koma): ")

# Split input: "Tulus, Hindia, Raisa"
artist_list = [a.strip() for a in artist_input.split(",") if a.strip()]

print("\n=== ARTIS YANG AKAN DISCRAPE ===")
for a in artist_list:
    print("-", a)

# Jalankan scraping satu per satu
for artist_name in artist_list:
    scrape_genius_artist(artist_name)

print("\n[✓] SEMUA ARTIS SELESAI DICRAWL DAN DISIMPAN KE CSV")
