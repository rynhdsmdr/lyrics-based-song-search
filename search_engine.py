import pandas as pd
from preprocess import preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
import numpy as np

# =============================
# LOAD RAW & CLEAN DATASET
# =============================
df_raw = pd.read_csv("dataset/lyrics_dataset.csv")      # artist,title,lyrics,image_url,genius_url
df_clean = pd.read_csv("dataset/songs_processed.csv")  # artist,title,image_url,genius_url,lyrics_clean

df_clean['lyrics_clean'] = df_clean['lyrics_clean'].fillna("")
df_raw['lyrics'] = df_raw['lyrics'].fillna("")

# Untuk search, pakai clean corpus
corpus_clean = df_clean['lyrics_clean'].astype(str).tolist()

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

def search_bm25(query):
    processed_query = preprocess(query)
    tokens = processed_query.split()

    scores = bm25.get_scores(tokens)
    df_clean["bm25_score"] = scores

    # ambil index row
    ranked = df_clean.sort_values(by="bm25_score", ascending=False).head(10)

    results = []
    for idx, row in ranked.iterrows():
        # gunakan idx untuk ambil data RAW
        raw = df_raw.iloc[idx]

        results.append({
            "artist": raw['artist'],
            "title": raw['title'],
            "lyrics": raw['lyrics'],                # <<< RAW LYRICS
            "image_url": raw['image_url'],
            "genius_url": raw['genius_url'],
            "score": float(row['bm25_score'])
        })

    return results

def search_tfidf(query):
    processed_query = preprocess(query)

    query_vec = tfidf_vectorizer.transform([processed_query])
    cosine_sim = (tfidf_matrix @ query_vec.T).toarray().ravel()

    df_clean["tfidf_score"] = cosine_sim

    ranked = df_clean.sort_values(by="tfidf_score", ascending=False).head(10)

    results = []
    for idx, row in ranked.iterrows():
        raw = df_raw.iloc[idx]

        results.append({
            "artist": raw['artist'],
            "title": raw['title'],
            "lyrics": raw['lyrics'],                 # <<< RAW LYRICS
            "image_url": raw['image_url'],
            "genius_url": raw['genius_url'],
            "score": float(row['tfidf_score'])
        })

    return results
