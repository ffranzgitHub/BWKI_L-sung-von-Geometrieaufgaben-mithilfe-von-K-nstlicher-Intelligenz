# Code aus dem Buch "Natural Language Processing mit PyTorch (O'Reilly)"
# Code unter https://github.com/joosthub/PyTorchNLPBook verfügbar

import numpy as np
import string
from vocabulary import aufgabenVocabulary
from collections import Counter

class aufgabenVectorizer():
    """ The Vectorizer which coordinates the Vocabularies and puts them to use"""
    def __init__(self, aufgabe_vocab, class_vocab):
        """
        Args:
            aufgabe_vocab (augfabenVocabulary): maps words to integers
            class_vocab (augfabenVocabulary): maps class labels to integers
        """
        self.aufgabe_vocab = aufgabe_vocab
        self.class_vocab = class_vocab

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
    def from_dataframe(cls, aufgabe_df, cutoff=25):
        """Instantiate the vectorizer from the dataset dataframe
        
        Args:
            aufgabe_df (pandas.DataFrame): the review dataset
            cutoff (int): the parameter for frequency-based filtering
        Returns:
            an instance of the ReviewVectorizer
        """
        aufgabe_vocab = aufgabenVocabulary(add_unk=True)
        class_vocab = aufgabenVocabulary(add_unk=False)
        
        # Add ratings
        for rating in sorted(set(aufgabe_df.rating)):
            class_vocab.add_token(rating)

        # Add top words if count > provided count
        word_counts = Counter()
        for review in aufgabe_df.review:
            for word in review.split(" "):
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
        aufgabe_vocab = aufgabenVocabulary.from_serializable(contents['aufgabe_vocab'])
        class_vocab =  aufgabenVocabulary.from_serializable(contents['class_vocab'])

        return cls(aufgabe_vocab=aufgabe_vocab, class_vocab=class_vocab)

    def to_serializable(self):
        """Create the serializable dictionary for caching
        
        Returns:
            contents (dict): the serializable dictionary
        """
        return {'aufgabe_vocab': self.aufgabe_vocab.to_serializable(),
                'class_vocab': self.class_vocab.to_serializable()}