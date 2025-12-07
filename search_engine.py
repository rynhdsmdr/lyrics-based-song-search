import pandas as pd
from preprocess import preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
import numpy as np

# =============================
# LOAD DISPLAY & SEARCH DATASET
# =============================
df_display = pd.read_csv("dataset/clean.csv")      # artist,title,lyrics,image_url,genius_url
df_search = pd.read_csv("dataset/search_dataset.csv")         # artist,title,image_url,genius_url,lyrics_clean

df_search['lyrics_clean'] = df_search['lyrics_clean'].fillna("")
df_display['lyrics'] = df_display['lyrics'].fillna("")

# Corpus untuk search (clean)
corpus_clean = df_search['lyrics_clean'].astype(str).tolist()

# =============================
# PREPROCESS CORPUS
# =============================
processed_corpus = [preprocess(text) for text in corpus_clean]

# Tokenized corpus for BM25
tokenized_corpus = [doc.split() for doc in processed_corpus]
bm25 = BM25Okapi(tokenized_corpus)

# TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(processed_corpus)


# ==================================================
#  FUNGSI UNTUK CEK EXACT MATCH JUDUL LAGU
# ==================================================
def check_exact_title_match(query):
    q = query.strip().lower()

    match = df_display[df_display["title"].str.lower() == q]

    if len(match) == 0:
        return None

    row = match.iloc[0]

    # return hasil prioritas pertama
    return {
        "artist": row["artist"],
        "title": row["title"],
        "lyrics": row["lyrics"],
        "image_url": row["image_url"],
        "genius_url": row["genius_url"],
        "score": 99999  # highest score to push at top
    }


# ==================================================
#  SEARCH BM25 (DENGAN PRIORITAS CARI JUDUL)
# ==================================================
def search_bm25(query):
    processed_query = preprocess(query)
    tokens = processed_query.split()

    # CEK EXACT MATCH JUDUL
    exact = check_exact_title_match(query)
    used_titles = set()

    results = []

    if exact:  # Jika judul cocok persis → taruh paling atas
        results.append(exact)
        used_titles.add(exact["title"].lower())

    # BM25 ranking
    scores = bm25.get_scores(tokens)
    df_search["bm25_score"] = scores
    ranked = df_search.sort_values(by="bm25_score", ascending=False)

    # lanjut ambil ranking BM25
    for idx, row in ranked.iterrows():
        raw = df_display.iloc[idx]

        # Skip jika sudah masuk result (judul sama)
        if raw["title"].lower() in used_titles:
            continue

        results.append({
            "artist": raw['artist'],
            "title": raw['title'],
            "lyrics": raw['lyrics'],  # RAW LYRICS untuk display
            "image_url": raw['image_url'],
            "genius_url": raw['genius_url'],
            "score": float(row['bm25_score'])
        })

        if len(results) == 10:
            break

    return results


# ==================================================
#  SEARCH TF-IDF (DENGAN PRIORITAS CARI JUDUL)
# ==================================================
def search_tfidf(query):
    processed_query = preprocess(query)

    query_vec = tfidf_vectorizer.transform([processed_query])
    cosine_sim = (tfidf_matrix @ query_vec.T).toarray().ravel()

    df_search["tfidf_score"] = cosine_sim
    ranked = df_search.sort_values(by="tfidf_score", ascending=False)

    # CEK EXACT MATCH JUDUL
    exact = check_exact_title_match(query)
    used_titles = set()
    results = []

    if exact:
        results.append(exact)
        used_titles.add(exact["title"].lower())

    for idx, row in ranked.iterrows():
        raw = df_display.iloc[idx]

        if raw["title"].lower() in used_titles:
            continue

        results.append({
            "artist": raw['artist'],
            "title": raw['title'],
            "lyrics": raw['lyrics'],  # RAW
            "image_url": raw['image_url'],
            "genius_url": raw['genius_url'],
            "score": float(row['tfidf_score'])
        })

        if len(results) == 10:
            break

    return results
