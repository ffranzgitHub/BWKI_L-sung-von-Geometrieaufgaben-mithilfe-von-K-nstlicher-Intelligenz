import json
from globale_Variablen import globale_variablen

from Daten_Laden.dataset import aufgabenDataset
from Daten_Laden.text_to_minibatches import generate_batches

PATH = globale_variablen.get("path_to_data")

def load_data():
    with open(PATH, "r") as file:
        json_data = json.loads(file.read())

        __add_split(json_data)
        dataset = aufgabenDataset.load_dataset_and_make_vectorizer(json_data)
        batches = generate_batches(dataset=dataset, batch_size=dataset.get_num_batches(), device=globale_variablen.get("device"))

        return batches

def __add_split(data):
    '''die Funktion verändert die Json Variable selbst
    
    Args:
        data: (Json List,dic) 
    '''
    for dic in data[:18]:
        dic["split"] = "train"
    for dic in data[18:21]:
        dic["split"] = "val"
    for dic in data[21:]:
        dic["split"] = "test"

    # TODO: die Aufteilung muss ganz zufällig sein
    # TODO: Die Vehältnisse zwischen test/val/train müssen übergeben werden
    # Hyperparameter benutzen