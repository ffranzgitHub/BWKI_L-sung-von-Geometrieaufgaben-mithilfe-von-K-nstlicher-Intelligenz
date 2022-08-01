'''
die Datei ist dafür da, Aufgaben manuell (also wie im echten Endprogramm) einzugeben
'''
from Daten_Laden.dataset import aufgabenDataset

VECTORIZER_PATH = "gespeicherte_Klassen/vectorizer"

GENZWERT_UNK_VERHÄLTNISS = 0.2

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
    if verhältniss <= GENZWERT_UNK_VERHÄLTNISS:
        print("akzeptiert: {} von {}".format(unk_number, aufgabe_count))
    else:
        print("nicht akzeptiert: {} von {}".format(unk_number, aufgabe_count))