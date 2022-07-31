# Code aus dem Buch "Natural Language Processing mit PyTorch (O'Reilly)"
# Code unter https://github.com/joosthub/PyTorchNLPBook verfügbar

from torch.utils.data import Dataset
import pandas as pd
import json
from vectorizer import aufgabenVectorizer

class aufgabenDataset(Dataset):
    '''
    benötigt einen Pandas DataFrame mit einer Spalte für mit train/val/test

    torch.utils.data.Dataset ist ein "abstrakter Iterator", der von dem DataLoader gewrappt wird. Das heißt
    es müssen die Funktionen __len__() und __getitem__() überschrieben werden
    '''
    def __init__(self, aufgabe_df, vectorizer):
        """
        Args:
            aufgabe_df (pandas.DataFrame): the dataset
            vectorizer (aufgabenVectorizer): vectorizer instantiated from dataset
        """
        self.aufgabe_df = aufgabe_df
        self._vectorizer = vectorizer

        self.train_df = self.aufgabe_df[self.aufgabe_df.split=='train']
        self.train_size = len(self.train_df)

        self.val_df = self.aufgabe_df[self.aufgabe_df.split=='val']
        self.validation_size = len(self.val_df)

        self.test_df = self.aufgabe_df[self.aufgabe_df.split=='test']
        self.test_size = len(self.test_df)

        self._lookup_dict = {'train': (self.train_df, self.train_size),
                             'val': (self.val_df, self.validation_size),
                             'test': (self.test_df, self.test_size)}

        self.set_split('train')

    @classmethod
    def load_dataset_and_make_vectorizer(cls, aufgaben_json):
        """Load dataset and make a new vectorizer from scratch
        
        Args:
            aufgaben_json (json): location of the dataset
        Returns:
            an instance of ReviewDataset
        """
        train_aufgabe_json = aufgaben_json[aufgabe_df.split=='train']
        return cls(aufgabe_df, aufgabenVectorizer.from_dataframe(train_aufgabe_df))
    
    @classmethod
    def load_dataset_and_load_vectorizer(cls, aufgaben_json, vectorizer_filepath):
        """Load dataset and the corresponding vectorizer. 
        Used in the case in the vectorizer has been cached for re-use
        
        Args:
            aufgaben_json (str): location of the dataset
            vectorizer_filepath (str): location of the saved vectorizer
        Returns:
            an instance of ReviewDataset
        """
        aufgabe_df = pd.read_csv(aufgaben_json)
        vectorizer = cls.load_vectorizer_only(vectorizer_filepath)
        return cls(aufgabe_df, vectorizer)

    @staticmethod
    def load_vectorizer_only(vectorizer_filepath):
        """a static method for loading the vectorizer from file
        
        Args:
            vectorizer_filepath (str): the location of the serialized vectorizer
        Returns:
            an instance of ReviewVectorizer
        """
        with open(vectorizer_filepath) as fp:
            return aufgabenVectorizer.from_serializable(json.load(fp))

    def save_vectorizer(self, vectorizer_filepath):
        """saves the vectorizer to disk using json
        
        Args:
            vectorizer_filepath (str): the location to save the vectorizer
        """
        with open(vectorizer_filepath, "w") as fp:
            json.dump(self._vectorizer.to_serializable(), fp)

    def get_vectorizer(self):
        """ returns the vectorizer """
        return self._vectorizer

    def set_split(self, split="train"):
        """ selects the splits in the dataset using a column in the dataframe 
        
        Args:
            split (str): one of "train", "val", or "test"
        """
        self._target_split = split
        self._target_df, self._target_size = self._lookup_dict[split]

    def __len__(self):
        return self._target_size

    def __getitem__(self, index):
        """the primary entry point method for PyTorch datasets
        
        Args:
            index (int): the index to the data point 
        Returns:
            a dictionary holding the data point's features (x_data) and label (y_target)
        """
        row = self._target_df.iloc[index]

        review_vector = \
            self._vectorizer.vectorize(row.review)

        rating_index = \
            self._vectorizer.rating_vocab.lookup_token(row.rating)

        return {'x_data': review_vector,
                'y_target': rating_index}

    def get_num_batches(self, batch_size):
        """Given a batch size, return the number of batches in the dataset
        
        Args:
            batch_size (int)
        Returns:
            number of batches in the dataset
        """
        return len(self) // batch_size  
    
