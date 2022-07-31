import json
'''
Funktion: Laden der Daten, Tokens und Aufgabentyen(Klassen) "zählen"

TODO:überflüssig, wird von den Dateien in Daten Laden übernommen
'''

with open("daten/Aufgaben_Serlo_Json.json", "r") as read_file:
    aufgaben = json.load(read_file)

    all_words = []
    classes = []

    new_json = []
    for aufgabe in aufgaben:

        new_json.append(aufgabe)
        aufgaben_text = aufgabe["Text"]

        for word in aufgaben_text.split(" "):
            if word not in all_words:
                all_words.append(word)
        if aufgabe["Aufgabentyp"] not in classes:
            classes.append(aufgabe["Aufgabentyp"])    