from Daten_Laden.text_to_minibatches import generate_batches
from Daten_Laden.split_dataset import _add_split
import json
from Daten_Laden.dataset import aufgabenDataset
import os
from itertools import cycle

PATH = "daten/Aufgaben_Serlo_Json.json"

with open(PATH, "r") as file:
    json_data = json.loads(file.read())

    _add_split(json_data)
    dataset = aufgabenDataset.load_dataset_and_make_vectorizer(json_data)
    x = generate_batches(dataset=dataset, batch_size=1)
    x = cycle(x) # Wenn alle Batches durchgegangen wurden, wird wieder beim ersten Batch gestartet

    erster_batch = next(x)
    print(erster_batch)

    input_size = len(erster_batch["x_data"][0])
    num_classes = len(erster_batch["y_target"]) # TODO das gilt nur, wenn das y_target One-Hot encoded ist. Aktuell ist das aber nicht der Fall