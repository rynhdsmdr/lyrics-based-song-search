import nltk

# Download hanya sekali saat preprocessing dijalankan
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("wordnet")

from preprocess import preprocess
