'''
die Datei ist dafür da, Aufgaben manuell (also wie im echten Endprogramm) einzugeben
'''
from globale_Variablen import globale_variablen
from Daten_Laden.dataset import aufgabenDataset
from Netz.model import AufgabenDetector
from Daten_Laden.data import create_dataset
from Vorverarbeitung.stemming import bag_of_words, tokenize
from Vorverarbeitung.convert_value_to_NE_regex import named_entities
from Loesen_Der_Aufgaben.loesen import pythagoras
import torch

VECTORIZER_PATH = globale_variablen.get("path_to_saved_vectorizer")

GRENZWERT_UNK_VERHÄLTNISS = 0.2

if __name__ == "__main__":
    vectorizer = aufgabenDataset.load_vectorizer_only(VECTORIZER_PATH)
    aufgabe = "Ein rechtwinkliges Dreieck hat die Katheten a=3 und b=4 Berechne die Hypothenuse" #input("gib die Aufgabe ein: ")
    
    # zähle Gesammttokenanzahl der Aufgabe
    tokens = aufgabe.split(" ")
    aufgabe_count = len(tokens)
    # Problem: vectorize gibt einen one-hot encodeten Vector zurück (also zähl
    # er nicht mit wie viele unknwon Tokens es gibt)
    unk_number = vectorizer.count_unknown(aufgabe)

    verhältniss = unk_number / aufgabe_count
    if verhältniss <= GRENZWERT_UNK_VERHÄLTNISS:
        print("Aktzeptiert! Unbekannte Wörter: {} von {}".format(unk_number, aufgabe_count))
    else:
        print("Nicht aktzeptiert! Unbekannte Wörter: {} von {}".format(unk_number, aufgabe_count))

    # TODO: Ich habe eine Aufgabe gestellt die 1:1 in der json steht und trotzdem wird angegeben
    # Dass zu viele Wörter unbekannt sind
    # Vielleicht sollten wir alle Wörter lowern?


    dataset = create_dataset()
    all_words = [word for word in dataset.get_vectorizer().aufgabe_vocab._idx_to_token.values()] 
    # Diese Iteration wird benötigt um aus Dict_Values([1, 2, 3]) --> [1, 2, 3] zu machen
    # Aus mir unbekannten Gründen nimmt das stemming/bag_of_words Dict_Values([1, 2, 3]) nicht an
    
    input_size = len(all_words) 
    hidden_size = globale_variablen.get("hidden_size")
    num_classes = len(dataset.get_vectorizer().class_vocab) 

    model = AufgabenDetector(input_size, hidden_size, num_classes) 
    model.load_state_dict(torch.load(globale_variablen["path_to_model"]))
    model.eval()


    input_x = tokenize(aufgabe)
    input_x = bag_of_words(input_x, all_words, performe_stem=False, filter_stop_words=False)
    input_x = torch.tensor(input_x)

    softmax = torch.nn.Softmax(dim=0)
    out = model(input_x)
    out = softmax(out)
    result = dataset.get_vectorizer().class_vocab._idx_to_token[torch.argmax(out).item()]

    angepasster_satz, entities = named_entities(aufgabe)
    entities = dict(entities)

    if result == "Satz des Pythagoras":
        pythagoras(entities)

    else:
        print("Aufgabenlösung für diesen Typen noch nicht implementiert")

    print()


    # print(f"{'' if verhältniss <= GRENZWERT_UNK_VERHÄLTNISS else 'nicht '}aktzeptiert: {unk_number} von {aufgabe_count}")
    # Das wäre eine etwas kürzere Alternative