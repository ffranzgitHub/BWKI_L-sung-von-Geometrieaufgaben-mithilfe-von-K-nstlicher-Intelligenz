import json
from Vorverarbeitung.convert_value_to_NE_regex import named_entities

with open("Aufgaben und Kategorien/Aufgaben_Serlo_Json.json", "r") as read_file:
    aufgaben = json.load(read_file)

    all_words = []
    classes = []

    new_json = []
    for aufgabe in aufgaben:
        aufgabe = aufgabe[0]

        new_json.append(aufgabe)
        aufgaben_text = aufgabe["Text"]
        #named_entities(aufgaben_text) --> auskommentiert, weil es Probleme mit dem Import der named_entities() funltion gab

        for word in aufgaben_text.split(" "):
            if word not in all_words:
                all_words.append(word)
        if aufgabe["Aufgabentyp"] not in classes:
            classes.append(aufgabe["Aufgabentyp"])    

    #print(new_json)    --> falls wir die Listen um die Aufgaben entfernen wollen
    print(all_words)
    print(classes)

    #print(emps[0][0].get("Ja-Nein Frage"))