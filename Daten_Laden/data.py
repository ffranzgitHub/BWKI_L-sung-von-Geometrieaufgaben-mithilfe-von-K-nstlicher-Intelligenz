from numpy import unique
from globale_Variablen import globale_variablen
import json
from Daten_Laden.dataset import aufgabenDataset
import random

def __add_split(data):
    '''die Funktion verändert die Json Variable selbst
    Args:
        data: (Json List,dic) 
    '''
    # sorted_data erstellen mit {"Aufgabentpy1": ["text1", "text2"], "Aufgabentyp2", [text3, text4]}
    classes = unique([d.get("Aufgabentyp") for d in data])
    sorted_data = {}
    for aufgabe in classes:
        sorted_data[aufgabe] = []
    for datenpunkt in data:
        sorted_data[datenpunkt["Aufgabentyp"]].append(datenpunkt["Text"])

    # The split must be random and include all classes equaly in all splits
    random.shuffle(data)
    for dic in data[:18]:
        dic["split"] = "train"
    for dic in data[18:21]:
        dic["split"] = "val"
    for dic in data[21:]:
        dic["split"] = "test"

    # TODO: die Aufteilung muss ganz zufällig sein
    # TODO: Die Vehältnisse zwischen test/val/train müssen übergeben werden
    # Hyperparameter benutzen

def create_dataset():
    PATH = globale_variablen.get("path_to_data")
    with open(PATH, "r") as file:
        json_data = json.loads(file.read())

    __add_split(json_data)
    dataset = aufgabenDataset.load_dataset_and_make_vectorizer(json_data)

    return dataset
