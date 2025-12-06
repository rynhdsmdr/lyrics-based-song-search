import requests
from bs4 import BeautifulSoup

def extract_lyrics(url):
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")

        divs = soup.select("div[data-lyrics-container='true']")
        lyrics = "\n".join([d.get_text(separator="\n") for d in divs])

        return lyrics.strip()

    except:
        return ""
