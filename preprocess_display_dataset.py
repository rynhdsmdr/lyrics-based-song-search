import csv
import re

def clean_lyrics(raw_lyrics: str) -> str:
    text = raw_lyrics

    # 1. Hapus “11 Contributors”, “1Contributor”, dll
    text = re.sub(r'\d+\s*Contributors?', '', text, flags=re.IGNORECASE)

    # 2. Hapus header seperti "Monokrom Lyrics", "Song Lyrics", dll
    text = re.sub(r'.*Lyrics', '', text, flags=re.IGNORECASE)

    # 3. Hapus semua bracket section [Verse 1], [Chorus], [Bridge], dll
    text = re.sub(r'\[.*?\]', '', text)

    # 4. Hapus baris kosong berlebihan
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]

    return "\n".join(lines)

# =====================
# CLEAN CSV
# =====================

input_csv = "dataset/lyrics_dataset.csv"
output_csv = "dataset/clean.csv"

with open(input_csv, "r", encoding="utf-8") as f_in, \
     open(output_csv, "w", encoding="utf-8", newline="") as f_out:

    reader = csv.DictReader(f_in)
    fieldnames = ["artist", "title", "lyrics", "image_url", "genius_url"]
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        cleaned = clean_lyrics(row["lyrics"])
        row["lyrics"] = cleaned
        writer.writerow(row)

print("✔ Semua lirik sudah dibersihkan dan disimpan ke dataset_clean.csv")
