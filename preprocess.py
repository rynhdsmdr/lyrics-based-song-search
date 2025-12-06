import re
from langdetect import detect
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag, word_tokenize

factory = StemmerFactory()
stem_id = factory.create_stemmer()
lemma_en = WordNetLemmatizer()

# ================================
# REMOVE SLANG (opsional)
# ================================
slang_map = {
    "gak": "tidak",
    "ga": "tidak",
    "gk": "tidak",
    "ngga": "tidak",
    "gila": "gila",
}

def normalize_slang(text):
    for slang, correct in slang_map.items():
        text = text.replace(slang, correct)
    return text


# ================================
# DETECT POS (English Lemma)
# ================================
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


# ================================
# CLEANING FUNCTION
# ================================
def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = normalize_slang(text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ================================
# LEMMATIZE ENGLISH
# ================================
def lemmatize_english(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    lemma = [lemma_en.lemmatize(w, get_wordnet_pos(t)) for w, t in tagged]
    return " ".join(lemma)


# ================================
# FINAL PREPROCESS
# ================================
def preprocess(text):
    text = clean_text(text)

    if text.strip() == "":
        return ""

    try:
        lang = detect(text)
    except:
        lang = "unknown"

    if lang == "id":
        return stem_id.stem(text)
    else:
        return lemmatize_english(text)
