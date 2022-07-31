from text_to_minibatches import generate_batches
from split_dataset import _add_split
import json
from dataset import aufgabenDataset
import os

PATH = "daten/Aufgaben_Serlo_Json.json"

with open(PATH, "r") as file:
    json_data = json.loads(file.read())

    _add_split(json_data)
    dataset = aufgabenDataset.load_dataset_and_make_vectorizer(json_data)
    x = generate_batches(dataset=dataset, batch_size=1)

    print(next(x))