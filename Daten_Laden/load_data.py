from Daten_Laden.text_to_minibatches import generate_batches
from Daten_Laden.split_dataset import _add_split
import json
from Daten_Laden.dataset import aufgabenDataset
import torch

#TODO: Globale Variablen speichern
PATH = "daten/Aufgaben_Serlo_Json.json"

def load_data():
    with open(PATH, "r") as file:
        json_data = json.loads(file.read())

        _add_split(json_data)
        dataset = aufgabenDataset.load_dataset_and_make_vectorizer(json_data)
        batches = generate_batches(dataset=dataset, batch_size=1)

        return batches