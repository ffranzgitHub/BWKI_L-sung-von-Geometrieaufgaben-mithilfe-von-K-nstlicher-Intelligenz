
if __name__ == "__main__":
    from numpy import unique
    import json
    import random

    globale_variablen = \
        {
            "split_train": 0.8,
            "split_val": 0.1,
            "split_test": 0.1
        }
else:
    from numpy import unique
    from globale_Variablen import globale_variablen
    import json
    from Daten_Laden.dataset import aufgabenDataset
    import random
    from Vorverarbeitung.convert_value_to_NE_regex import variablenzuweisung_extrahieren
    from Vorverarbeitung.stemming import stem, ignore_stop_words, tokenize


def __klassenanzahl_in_split(sorted_data: dict):
    '''rechnet aus den Verhältnissen der Splits und der Anzahl der Elemente in einer Klasse die konkrete Aufteilung aus'''
    gesammtlaenge = 0
    for array in sorted_data.values():
        gesammtlaenge += len(array)  # Gesammtlänge der Daten

    # Anzahl Aufgabenn für Train, Val und Test von jedem Aufgabentyp
    train_n_classes = {}
    for aufgabentyp, aufgaben in sorted_data.items():
        anzahl_aufgaben = len(aufgaben)
        train_n_classes[aufgabentyp] = round(
            globale_variablen["split_train"]*anzahl_aufgaben)

    # für alle val
    # val wird abgerundet (außer es ist 0, dann 1)
    val_n_classes = {}
    for aufgabentyp, aufgaben in sorted_data.items():
        anzahl_aufgaben = len(aufgaben)
        val_n_classes[aufgabentyp] = round(
            globale_variablen["split_val"]*anzahl_aufgaben)

    # für alle test
    # test bekommt den Rest (außer es ist 0, dann 1 und train-1)
    test_n_classes = {}
    for n_train, n_val, aufgabentyp, aufgaben in zip(train_n_classes.values(), val_n_classes.values(), sorted_data.keys(), sorted_data.values()):
        anzahl_aufgaben = len(aufgaben)
        if anzahl_aufgaben-n_train-n_val > 0:
            test_n_classes[aufgabentyp] = anzahl_aufgaben-n_train-n_val
        else:
            test_n_classes[aufgabentyp] = 1
            n_train -= 1

    """
    Warum Test den Rest bekommt und wir nicht einfach Runden:
    Datenverlust: 
    0.33 * 10 = 3
    0.33 * 10 = 3
    0.33 * 10 = 3 
    3 + 3 + 3 = 9 != 10
    """

    return train_n_classes, val_n_classes, test_n_classes


def __add_split(data):
    '''die Funktion fügt jedem Datenpunkt einem Split (train/val/test) hinzu
    Args:
        data: (Json List,dic) 
    '''
    # The split must be random and include all classes equaly in all parts
    # sorted_data erstellen mit {"Aufgabentpy1": ["text1", "text2"], "Aufgabentyp2", [text3, text4]}
    sorted_data = dict.fromkeys(unique([d.get("Aufgabentyp") for d in data]), None)
    for datenpunkt in data:
        if not sorted_data[datenpunkt["Aufgabentyp"]]:
            sorted_data[datenpunkt["Aufgabentyp"]] = []
        sorted_data[datenpunkt["Aufgabentyp"]].append(datenpunkt["Text"])

    # TODO: random shuffle wird nicht benutzt (weil nur gezählt wird), eigentlich sollte data geshuffelt werden
    [random.shuffle(liste) for liste in sorted_data.values()]  # zufällig

    train_classes_counters, val_classes_counters, test_classes_counters = __klassenanzahl_in_split(
        sorted_data)

    for datapoint in data:
        if train_classes_counters[datapoint["Aufgabentyp"]] > 0:
            train_classes_counters[datapoint["Aufgabentyp"]] -= 1
            datapoint["split"] = "train"

        elif val_classes_counters[datapoint["Aufgabentyp"]] > 0:
            val_classes_counters[datapoint["Aufgabentyp"]] -= 1
            datapoint["split"] = "val"

        elif test_classes_counters[datapoint["Aufgabentyp"]] > 0:
            test_classes_counters[datapoint["Aufgabentyp"]] -= 1
            datapoint["split"] = "test"

        else:
            # TODO: richtigen Error Raisen
            print("ERROR")


def create_dataset(json_data):
    __add_split(json_data)
    dataset = aufgabenDataset.load_dataset_and_make_vectorizer(json_data)

    return dataset


def vorverarbeitung_und_dataset():
    PATH = globale_variablen.get("path_to_data")
    with open(PATH, "r") as file:
        json_data = json.loads(file.read())

    for aufgaben_dic in json_data:
        aufgaben_dic["Text"], _ = variablenzuweisung_extrahieren(aufgaben_dic["Text"])

        aufgaben_dic_text_liste = aufgaben_dic["Text"].split(" ")
        aufgaben_dic_text_liste = [stem(word) for word in aufgaben_dic_text_liste]
        aufgaben_dic_text_liste = ignore_stop_words(aufgaben_dic_text_liste)

        aufgaben_dic["Text"] = " ".join(aufgaben_dic_text_liste)

    dataset = create_dataset(json_data)

    return dataset


if __name__ == "__main__":
    data = [
        {"Text": f"t{i}", "Aufgabentyp": f"a{random.randint(1,3)}"} for i in range(100)]

    __add_split(data)
