'''
die Datei ist dafür da, Aufgaben manuell (also wie im echten Endprogramm) einzugeben
'''
from globale_Variablen import globale_variablen
from Daten_Laden.dataset import aufgabenDataset

VECTORIZER_PATH = globale_variablen.get("path_to_saved_vectorizer")

GRENZWERT_UNK_VERHÄLTNISS = 0.2

if __name__ == "__main__":
    vectorizer = aufgabenDataset.load_vectorizer_only(VECTORIZER_PATH)
    aufgabe = input("gib die Aufgabe ein: ")
    # zähle Gesammttokenanzahl der Aufgabe
    tokens = aufgabe.split(" ")
    aufgabe_count = len(tokens)
    # Problem: vectorize gibt einen one-hot encodeten Vector zurück (also zähl
    # er nicht mit wie viele unknwon Tokens es gibt)
    unk_number = vectorizer.count_unknown(aufgabe)

    verhältniss = unk_number / aufgabe_count
    if verhältniss <= GRENZWERT_UNK_VERHÄLTNISS:
        print("aktzeptiert: {} von {}".format(unk_number, aufgabe_count))
    else:
        print("nicht aktzeptiert: {} von {}".format(unk_number, aufgabe_count))

    # print(f"{'' if verhältniss <= GRENZWERT_UNK_VERHÄLTNISS else 'nicht '}aktzeptiert: {unk_number} von {aufgabe_count}")
    # Das wäre eine etwas kürzere Alternative