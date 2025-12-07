import re
from langdetect import detect
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag, word_tokenize

# ============================================================
# SETUP
# ============================================================
factory = StemmerFactory()
stem_id = factory.create_stemmer()
lemma_en = WordNetLemmatizer()

# ============================================================
# KATA YANG WAJIB DIHAPUS
# ============================================================
remove_words = {
    "contributors", "contributor", "lirik", "lyrics", "lyric",
    "penulis", "verse", "chorus", "bridge",
    "produced", "written", "copyright",
    "translated", "song", "refrain", "translations"
}

def remove_custom_words(text):
    pattern = r"\b(" + "|".join(remove_words) + r")\b"
    return re.sub(pattern, " ", text)


# ============================================================
# HAPUS HEADER GENIUS
# ============================================================
def remove_header(text, title, artist):

    text = text.lower()
    title = title.lower().strip()
    artist = artist.lower().strip()

    # Angka pembuka "11 monokrom"
    text = re.sub(r"^\s*\d+\s+", " ", text)

    # Hapus judul & artis di awal
    if title:
        text = re.sub(rf"^{title}\b", " ", text)
        text = re.sub(rf"\b{title}\b", " ", text)
        text = re.sub(rf"{title}\s+lyrics", " ", text)

    if artist:
        text = re.sub(rf"^{artist}\b", " ", text)
        text = re.sub(rf"\b{artist}\b", " ", text)

    return text


# ============================================================
# NORMALISASI SLANG (lebih aman)
# ============================================================
slang_map = {
    r"\bgak\b": "tidak",
    r"\bga\b": "tidak",
    r"\bgk\b": "tidak",
    r"\bngga\b": "tidak",
    r"\bnggak\b": "tidak",
    r"\btdk\b": "tidak"
}

def normalize_slang(text):
    for slang, correct in slang_map.items():
        text = re.sub(slang, correct, text)
    return text


# ============================================================
# POS TAG MAP
# ============================================================
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    if tag.startswith('V'):
        return wordnet.VERB
    if tag.startswith('N'):
        return wordnet.NOUN
    if tag.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN


# ============================================================
# CLEAN BASE
# ============================================================
def clean_text(text, title="", artist=""):
    if not isinstance(text, str):
        return ""

    text = text.lower()

    # hapus header genius
    text = remove_header(text, title, artist)

    # hapus kata-kata tertentu
    text = remove_custom_words(text)

    # normalisasi slang
    text = normalize_slang(text)

    # hapus angka
    text = re.sub(r"\b\d+\b", " ", text)

    # hapus simbol
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # rapikan spasi
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# ENGLISH LEMMA
# ============================================================
def lemmatize_english(text):
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)
    return " ".join([lemma_en.lemmatize(w, get_wordnet_pos(t)) for w, t in tags])


# ============================================================
# FINAL PREPROCESS (versi sangat stabil)
# ============================================================
def preprocess(text, title="", artist=""):
    text = clean_text(text, title, artist)

    if not text.strip():
        return ""

    # --- Deteksi Bahasa dengan fallback ---
    try:
        lang = detect(text)
    except:
        lang = "unknown"

    # --- Override untuk kasus Indonesia ---
    indo_keywords = ["aku", "engkau", "kau", "kamu", "tidak", "lagi", "yang", "ini", "itu"]

    if lang == "en" and any(w in text.split() for w in indo_keywords):
        lang = "id"

    # --- Preprocessing final ---
    if lang == "id":
        return stem_id.stem(text)
    else:
        return lemmatize_english(text)
