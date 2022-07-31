import json
from stemming import bag_of_words, stem, tokenize, ignore_stop_words
import stemming
'''
# TODO: Die Vorverarbeitung Funktionalität kann vielleicht direkt in die Dataset Klasse 
intigiert werden
'''



with open("daten/Aufgaben_Serlo_Json.json", "r") as read_file:
    aufgaben = json.load(read_file)

    # TODO: Liste an Tokens/Klassen kann mit der Vocaublary Klasse realisiert werden
    all_words = [] # Liste mit allen Wörtern
    classes = [] # Liste mit Aufgabentypen

    for aufgabe in aufgaben:

        aufgaben_text = aufgabe["Text"]

        for word in aufgaben_text.split(" "):
            if word not in all_words:
                all_words.append(word)
        if aufgabe["Aufgabentyp"] not in classes:
            classes.append(aufgabe["Aufgabentyp"])    

all_words = [stemming.stem(word) for word in all_words]
all_words = ignore_stop_words(all_words)

# Ab hier ist nur testen. Kann also gelöscht werden, wenn du verstanden hast, wie das ganze funktioniert

test_sentence = "Ein rechtwinkliges Dreieck hat die Katheten: a=5cm und b=8cm Deine Aufgabe ist es nun die Hypothenuse zu berechnen"
tokenized_test_sentence = tokenize(test_sentence)
tokenized_test_sentence = ignore_stop_words(tokenized_test_sentence)

bag = bag_of_words(tokenized_test_sentence, all_words)

print(bag)
