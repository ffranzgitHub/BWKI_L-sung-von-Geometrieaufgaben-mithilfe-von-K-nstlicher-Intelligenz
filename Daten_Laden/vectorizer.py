# Code aus dem Buch "Natural Language Processing mit PyTorch (O'Reilly)"
# Code unter https://github.com/joosthub/PyTorchNLPBook verfügbar

import numpy as np
import string
from Daten_Laden.vocabulary import aufgabenVocabulary
from collections import Counter


class aufgabenVectorizer():
    """ The Vectorizer which coordinates the Vocabularies and puts them to use"""

    def __init__(self, aufgabe_vocab: aufgabenVocabulary, class_vocab: aufgabenVocabulary):
        """
        Args:
            aufgabe_vocab (augfabenVocabulary): maps words to integers
            class_vocab (augfabenVocabulary): maps class labels to integers
        """
        self.aufgabe_vocab = aufgabe_vocab
        self.class_vocab = class_vocab

    # TODO prüfen inwiefern sich diese Funktion mit der Stemmin.py überschneidet
    def vectorize(self, aufgabe):
        """Create a collapsed one-hot vector for the "aufgabe"

        Args:
            aufgabe (str): the "aufgabe" 
        Returns:
            one_hot (np.ndarray): the collapsed one-hot encoding 
        """
        one_hot = np.zeros(len(self.aufgabe_vocab), dtype=np.float32)

        for token in aufgabe.split(" "):
            if token not in string.punctuation:
                one_hot[self.aufgabe_vocab.lookup_token(token)] = 1

        return one_hot

    @classmethod
    def from_json(cls, aufgabe_json, cutoff=0):
        """Instantiate the vectorizer from the dataset dataframe

        Args:
            aufgabe_json (json): the review dataset
            cutoff (int): the parameter for frequency-based filtering
        Returns:
            an instance of the ReviewVectorizer
        """
        aufgabe_vocab = aufgabenVocabulary(add_unk=True)
        class_vocab = aufgabenVocabulary(add_unk=False)

        # Add ratings
        for aufgabentyp in sorted(set([value["Aufgabentyp"] for value in aufgabe_json])):
            class_vocab.add_token(aufgabentyp)

        # Add top words if count > provided count
        word_counts = Counter()
        for aufgabe in [value["Text"] for value in aufgabe_json]:
            for word in aufgabe.split(" "):
                if word not in string.punctuation:
                    word_counts[word] += 1

        for word, count in word_counts.items():
            if count > cutoff:
                aufgabe_vocab.add_token(word)

        return cls(aufgabe_vocab, class_vocab)

    @classmethod
    def from_serializable(cls, contents):
        """Instantiate a ReviewVectorizer from a serializable dictionary

        Args:
            contents (dict): the serializable dictionary
        Returns:
            an instance of the ReviewVectorizer class
        """
        aufgabe_vocab = aufgabenVocabulary.from_serializable(
            contents['aufgabe_vocab'])
        class_vocab = aufgabenVocabulary.from_serializable(
            contents['class_vocab'])

        return cls(aufgabe_vocab=aufgabe_vocab, class_vocab=class_vocab)

    def to_serializable(self):
        """Create the serializable dictionary for caching

        Returns:
            contents (dict): the serializable dictionary
        """
        return {'aufgabe_vocab': self.aufgabe_vocab.to_serializable(),
                'class_vocab': self.class_vocab.to_serializable()}

    def count_unknown(self, aufgabe):
        '''
        die Funktion zähl die unbekannten Tokens in einer Aufgabe und gibt sie zurück
        '''
        tokens = aufgabe.split(" ")
        unk_counter = 0
        for token in tokens:
            # TODO: schöner Abfrage, ob Token erkannt wurde (get_unk funktion in vocab)
            if self.aufgabe_vocab.lookup_token(token) == self.aufgabe_vocab.lookup_token("<UNK>"):
                unk_counter += 1
        return unk_counter
