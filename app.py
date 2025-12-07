from flask import Flask, render_template, request, redirect, url_for
from search_engine import search_bm25, search_tfidf
import re

app = Flask(__name__)

def get_snippet(full_lyrics, query, window=40):
    if not full_lyrics:
        return ""

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    match = pattern.search(full_lyrics)

    if not match:
        return full_lyrics[:window*2] + "..."

    start = max(0, match.start() - window)
    end = min(len(full_lyrics), match.end() + window)
    snippet = full_lyrics[start:end]

    return ("..." if start > 0 else "") + snippet + ("..." if end < len(full_lyrics) else "")

def highlight(text, query):
    if not text:
        return ""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f"<span class='highlight'>{m.group(0)}</span>", text)


@app.route("/", methods=["GET", "POST"])
def bm25_page():
    query = ""
    results = []

    if request.method == "POST":
        query = request.form.get("query")
        return redirect(url_for("bm25_page", q=query))

    if request.args.get("q"):
        query = request.args.get("q")
        results = search_bm25(query)

        for r in results:
            lyrics = r.get("lyrics", "")          # FIX
            snippet_raw = get_snippet(lyrics, query)
            r["snippet"] = highlight(snippet_raw, query)  # FIX

    return render_template("page_bm25.html",
                           query=query,
                           results=results)


@app.route("/tfidf", methods=["GET", "POST"])
def tfidf_page():
    query = ""
    results = []

    if request.method == "POST":
        query = request.form.get("query")
        return redirect(url_for("tfidf_page", q=query))

    if request.args.get("q"):
        query = request.args.get("q")
        results = search_tfidf(query)

        for r in results:
            lyrics = r.get("lyrics", "")          # FIX
            snippet_raw = get_snippet(lyrics, query)
            r["snippet"] = highlight(snippet_raw, query)  # FIX

    return render_template("page_tfidf.html",
                           query=query,
                           results=results)


if __name__ == "__main__":
    app.run(debug=True)
