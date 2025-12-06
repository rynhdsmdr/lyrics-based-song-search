from flask import Flask, render_template, request, redirect, url_for
from search_engine import search_bm25, search_tfidf

app = Flask(__name__)

# ============================
#   PAGE 1 – BM25
# ============================
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

    return render_template("page_bm25.html",
                           query=query,
                           results=results)


# ============================
#   PAGE 2 – TF-IDF
# ============================
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

    return render_template("page_tfidf.html",
                           query=query,
                           results=results)


if __name__ == "__main__":
    app.run(debug=True)
