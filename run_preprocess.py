import csv
from preprocess import preprocess

input_file = "dataset/lyrics_dataset.csv"         # CSV asli
output_file = "dataset/tes.csv"      # CSV hasil preprocessing

with open(input_file, "r", encoding="utf-8") as f_in, \
     open(output_file, "w", encoding="utf-8", newline="") as f_out:

    reader = csv.DictReader(f_in)
    fieldnames = ["artist", "title", "processed_lyrics", "image_url", "genius_url"]

    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        artist = row["artist"]
        title = row["title"]
        lyrics = row["lyrics"]

        processed = preprocess(lyrics, title=title, artist=artist)

        writer.writerow({
            "artist": artist,
            "title": title,
            "processed_lyrics": processed,
            "image_url": row["image_url"],
            "genius_url": row["genius_url"]
        })

print("CSV berhasil diproses →", output_file)
