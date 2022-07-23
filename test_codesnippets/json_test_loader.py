import json

with open("Aufgaben und Kategorien/Aufgaben_Serlo_Json.json", "r") as read_file:
    emps = json.load(read_file, )

    print(emps[0][0].get("Ja-Nein Frage"))