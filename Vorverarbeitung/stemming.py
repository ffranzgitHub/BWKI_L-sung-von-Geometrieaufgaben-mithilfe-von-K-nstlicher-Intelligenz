import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np
from globale_Variablen import globale_variablen


#nltk.download("punkt")
# Beim ersten ausführen des Scriptes

stemmer = PorterStemmer()

def get_stopwords():
    with open(globale_variablen["path_to_stopwords"]) as f:
        stop_words = [line for line in f if not line.startswith(";")].extend(["!", "?", "°"])
    return stop_words

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words, performe_stem=True, filter_stop_words=True):
    if performe_stem:
        tokenized_sentence = [stem(w) for w in tokenized_sentence] 

    if filter_stop_words:
        tokenized_sentence = ignore_stop_words(tokenized_sentence)

    return np.array([1.0 if word in tokenized_sentence else 0.0 for word in all_words], dtype=np.float32)

def ignore_stop_words(word_list):
    stop_words = get_stopwords()
    word_list = [word for word in word_list if word not in stop_words]
    return word_list