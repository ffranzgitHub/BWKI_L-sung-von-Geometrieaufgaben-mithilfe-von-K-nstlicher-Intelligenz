from regex import P
from text_to_minibatches import generate_batches
from split_dataset import _add_split
import json

PATH = "daten/Aufgaben_Serlo_Json.json"

with open(PATH, "r") as file:
    json_data = json.laods(file.read())

    _add_split(json_data)