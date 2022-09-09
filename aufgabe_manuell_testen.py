'''
die Datei ist dafür da, Aufgaben manuell (also wie im echten Endprogramm) einzugeben
'''
from globale_Variablen import globale_variablen
from Daten_Laden.dataset import aufgabenDataset
from Netz.model import AufgabenDetector
from Daten_Laden.data import vorverarbeitung_und_dataset
from Vorverarbeitung.stemming import bag_of_words, tokenize, stem, ignore_stop_words
from Vorverarbeitung.convert_value_to_NE_regex import variablenzuweisung_extrahieren
from Loesen_Der_Aufgaben.loesen import name_to_aufgabe, not_implemented
import torch
import os

VECTORIZER_PATH = globale_variablen.get("path_to_saved_vectorizer")

GRENZWERT_UNK_VERHÄLTNISS = globale_variablen.get("unk_threshold_percentage")

sonderzeichen_zu_ascii = \
    {
        "Ä" : "ae",
        "Ü": "ue",
        "Ö": "oe",
        "ä" : "ae",
        "ü": "ue",
        "ö": "oe",
        "ß": "ss"
    }

if __name__ == "__main__":
    vectorizer = aufgabenDataset.load_vectorizer_only(VECTORIZER_PATH)
    # input("gib die Aufgabe ein: ")
    aufgabe = ""
    print()
    aufgabe = "".join([sonderzeichen_zu_ascii.get(letter, letter) for letter in aufgabe]) 
    #aufgabe = "Nenne einen Winkel für den Gilt: sin(A) = 0.5"

    angepasster_satz, entities = variablenzuweisung_extrahieren(aufgabe)

    # zähle Gesammttokenanzahl der Aufgabe
    # Vorher werden die Tokens aber noch gestemmt und Stoppwörter ignoriert
    tokens = angepasster_satz.split(" ")
    tokens = [stem(word) for word in tokens]
    tokens = ignore_stop_words(tokens)

    aufgabe_count = len(tokens)
    unk_number = vectorizer.count_unknown(angepasster_satz)

    verhältniss = unk_number / aufgabe_count
    if verhältniss <= GRENZWERT_UNK_VERHÄLTNISS:
        print("Lösung vermutlich nicht fehlerhaft! Unbekannte Wörter: {} von {}".format(
            unk_number, aufgabe_count))
    else:
        print("Lösung vermutlich fehlerhaft! Unbekannte Wörter: {} von {}".format(
            unk_number, aufgabe_count))

    # TODO müssen wir das Dataset hier neu erstellen oder können wir das "von oben" nutzen?
    # Dann könnten wir vielleicht auch den Vectorizer direkt mitnutzen
    # und müssen nicht hier bag_of_words aufrufen

    dataset = vorverarbeitung_und_dataset()
    all_words = [word for word in dataset.get_vectorizer().aufgabe_vocab._idx_to_token.values()]
    # Diese Iteration wird benötigt um aus Dict_Values([1, 2, 3]) --> [1, 2, 3] zu machen
    # Aus mir unbekannten Gründen nimmt das stemming/bag_of_words Dict_Values([1, 2, 3]) nicht an

    input_size = len(all_words)
    hidden_size = globale_variablen.get("hidden_size")
    num_classes = len(dataset.get_vectorizer().class_vocab)

    model = AufgabenDetector(input_size, hidden_size, num_classes)
    progress_training_path = os.listdir(globale_variablen["path_to_progress"])[-1]
    progress_name = os.listdir(globale_variablen["path_to_progress"]+progress_training_path)[-1]
    model.load_state_dict(torch.load(globale_variablen["path_to_progress"]+progress_training_path+"/"+progress_name)["save_model"])
    model.eval()

    entities = dict(entities)
    input_x = tokenize(angepasster_satz)
    input_x = bag_of_words(input_x, all_words, performe_stem=False, filter_stop_words=False)
    input_x = torch.tensor(input_x)

    softmax = torch.nn.Softmax(dim=0)
    out = model(input_x)
    out = softmax(out)

    propability_of_result = f"{(torch.max(out).item() * 100):.2f}%"
    result = dataset.get_vectorizer().class_vocab._idx_to_token[torch.argmax(out).item()]
    print("Aufgabentyp: '" + result + "' mit einer Wahrscheinlichkeit von " + propability_of_result)

    name_to_aufgabe.get(result, not_implemented)(entities)

    print()

    # print(f"{'' if verhältniss <= GRENZWERT_UNK_VERHÄLTNISS else 'nicht '}aktzeptiert: {unk_number} von {aufgabe_count}")
    # Das wäre eine etwas kürzere Alternative
