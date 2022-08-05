# Code aus dem Buch "Natural Language Processing mit PyTorch (O'Reilly)"
# Code unter https://github.com/joosthub/PyTorchNLPBook verfügbar

from torch.utils.data import Dataset
import pandas as pd
import json
from Daten_Laden.vectorizer import aufgabenVectorizer

class aufgabenDataset(Dataset):
    '''
    benötigt einen Pandas DataFrame mit einer Spalte für mit train/val/test

    torch.utils.data.Dataset ist ein "abstrakter Iterator", der von dem DataLoader gewrappt wird. Das heißt
    es müssen die Funktionen __len__() und __getitem__() überschrieben werden
    '''
    def __init__(self, aufgaben_json, vectorizer):
        """
        Args:
            aufgaben_json (json List,Dic): the dataset
            vectorizer (aufgabenVectorizer): vectorizer instantiated from dataset
        """
        self.aufgaben_json = aufgaben_json
        self._vectorizer = vectorizer

        self.train_json = [element for element in self.aufgaben_json if element['split'] == 'train']
        self.train_size = len(self.train_json)

        self.val_json = [element for element in self.aufgaben_json if element['split'] == 'val']
        self.validation_size = len(self.val_json)

        self.test_json = [element for element in self.aufgaben_json if element['split'] == 'test']
        self.test_size = len(self.test_json)

        self._lookup_dict = {'train': (self.train_json, self.train_size),
                             'val': (self.val_json, self.validation_size),
                             'test': (self.test_json, self.test_size)}

        self.set_split('train')

    @classmethod
    def load_dataset_and_make_vectorizer(cls, aufgaben_json):
        """Load dataset and make a new vectorizer from scratch
        
        Args:
            aufgaben_json (json): location of the dataset
        Returns:
            an instance of ReviewDataset
        """
        train_json = [element for element in aufgaben_json if element['split'] == 'train']
        return cls(aufgaben_json, aufgabenVectorizer.from_json(train_json))
    
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
        aufgaben_json = pd.read_csv(aufgaben_json)
        vectorizer = cls.load_vectorizer_only(vectorizer_filepath)
        return cls(aufgaben_json, vectorizer)

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

    def get_vectorizer(self) -> aufgabenVectorizer:
        """ returns the vectorizer """
        return self._vectorizer

    def set_split(self, split="train"):
        """ selects the splits in the dataset using a column in the dataframe 
        
        Args:
            split (str): one of "train", "val", or "test"
        """
        self._target_split = split
        self._target_json, self._target_size = self._lookup_dict[split]

    def __len__(self):
        return self._target_size

    def __getitem__(self, index):
        """the primary entry point method for PyTorch datasets
        
        Args:
            index (int): the index to the data point 
        Returns:
            a dictionary holding the data point's features (x_data) and label (y_target)
        """
        row = self._target_json[index]

        aufgabe_vector = \
            self._vectorizer.vectorize(row["Text"])

        # es wird nur die, der Klasse zugewiesenen, Zahl zurückgegeben und nicht ein one-hot-encodeter 
        # Vektor, da die Loss die Zahl (als Index für die Klasse) auch akzeptiert und selbst one-hot-encodet
        class_index = \
            self._vectorizer.class_vocab.lookup_token(row["Aufgabentyp"])

        return {'x_data': aufgabe_vector,
                'y_target': class_index}

    def get_num_batches(self, batch_size):
        """Given a batch size, return the number of batches in the dataset
        
        Args:
            batch_size (int)
        Returns:
            number of batches in the dataset
        """
        return len(self) // batch_size  
    
