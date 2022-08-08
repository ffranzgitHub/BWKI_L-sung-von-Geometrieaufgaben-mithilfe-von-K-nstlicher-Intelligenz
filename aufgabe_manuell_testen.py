'''
die Datei ist dafür da, Aufgaben manuell (also wie im echten Endprogramm) einzugeben
'''
from globale_Variablen import globale_variablen
from Daten_Laden.dataset import aufgabenDataset
from Netz.model import AufgabenDetector
from Daten_Laden.data import vorverarbeitung_und_dataset
from Vorverarbeitung.stemming import bag_of_words, tokenize
from Vorverarbeitung.convert_value_to_NE_regex import named_entities
from Loesen_Der_Aufgaben.loesen import pythagoras
import torch

VECTORIZER_PATH = globale_variablen.get("path_to_saved_vectorizer")

GRENZWERT_UNK_VERHÄLTNISS = globale_variablen.get("unk_threashold_percentage")

if __name__ == "__main__":
    vectorizer = aufgabenDataset.load_vectorizer_only(VECTORIZER_PATH)
    # input("gib die Aufgabe ein: ")
    aufgabe = "Ein rechtwinkliges Dreieck hat die Katheten a=69cm und b=45cm und c=30cm Berechne die fehlende Kathete"

    angepasster_satz, entities = named_entities(aufgabe)

    # zähle Gesammttokenanzahl der Aufgabe
    tokens = angepasster_satz.split(" ")
    aufgabe_count = len(tokens)
    unk_number = vectorizer.count_unknown(angepasster_satz)

    verhältniss = unk_number / aufgabe_count
    if verhältniss <= GRENZWERT_UNK_VERHÄLTNISS:
        print("Aktzeptiert! Unbekannte Wörter: {} von {}".format(
            unk_number, aufgabe_count))
    else:
        print("Nicht aktzeptiert! Unbekannte Wörter: {} von {}".format(
            unk_number, aufgabe_count))

    # TODO: Ich habe eine Aufgabe gestellt die 1:1 in der json steht und trotzdem wird angegeben
    # Dass zu viele Wörter unbekannt sind
    # Vielleicht sollten wir alle Wörter lowern?

    dataset = vorverarbeitung_und_dataset()
    all_words = [word for word in dataset.get_vectorizer(
    ).aufgabe_vocab._idx_to_token.values()]
    # Diese Iteration wird benötigt um aus Dict_Values([1, 2, 3]) --> [1, 2, 3] zu machen
    # Aus mir unbekannten Gründen nimmt das stemming/bag_of_words Dict_Values([1, 2, 3]) nicht an

    input_size = len(all_words)
    hidden_size = globale_variablen.get("hidden_size")
    num_classes = len(dataset.get_vectorizer().class_vocab)

    model = AufgabenDetector(input_size, hidden_size, num_classes)
    model.load_state_dict(torch.load(globale_variablen["path_to_model"]))
    model.eval()

    
    entities = dict(entities)
    input_x = tokenize(angepasster_satz)
    input_x = bag_of_words(
        input_x, all_words, performe_stem=False, filter_stop_words=False)
    input_x = torch.tensor(input_x)

    softmax = torch.nn.Softmax(dim=0)
    out = model(input_x)
    out = softmax(out)
    result = dataset.get_vectorizer(
    ).class_vocab._idx_to_token[torch.argmax(out).item()]

    if result == "Satz des Pythagoras":
        pythagoras(entities)
    else:
        print("Aufgabenlösung für diesen Typen noch nicht implementiert")

    print()

    # print(f"{'' if verhältniss <= GRENZWERT_UNK_VERHÄLTNISS else 'nicht '}aktzeptiert: {unk_number} von {aufgabe_count}")
    # Das wäre eine etwas kürzere Alternative
