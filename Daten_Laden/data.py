
if __name__=="__main__":
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


def __verhaeltnisse2anzahl(sorted_data):
    '''rechnet aus den Verhältnissen der Splits und der Anzahl der Elemente in einer Klasse die konkrete Aufteilung aus'''
    gesammtlaenge = 0
    for array in sorted_data.values(): gesammtlaenge += len(array)  #Gesammtlänge der Daten

    #Split Verhältnisse(p) zu Anzahlen(n)

    # Verhältniss bei ungeraden Zahlen -> test und val werden aufgerundet, train nimmt den Rest
    test_n = round(gesammtlaenge*globale_variablen.get("split_test")+0.5) #rundet immer auf
    val_n = round(gesammtlaenge*globale_variablen.get("split_val")+0.5)
    train_n = gesammtlaenge-test_n-val_n   #nimmt den Rest

    # Anzahl(n) der Elemente der Klassen aus den Verhältnissen(p) in den Splits berechen


    n_classen = [len(cls_list) for cls_list in sorted_data.values()] #Verhältnisse der Klassen
    p_classen = [n_classe/gesammtlaenge for n_classe in n_classen]



    #Anzahl der Elemente von den Klassen in den Splits
    #für alle train
    #ungerade Zahlen werden beim Train aufgerundet
    train_n_classen = []
    for p_class in p_classen:
        train_n_classen.append(round(train_n*p_class+0.5))
    #für alle val
    #val wird abgerundet (außer es ist 0, dann 1)
    val_n_classen = []
    for p_class in p_classen:
        val_n_classen.append(int(val_n*p_class) if int(val_n*p_class) > 0 else 1)
    #für alle test
    #test bekommt den Rest (außer es ist 0, dann 1 und train-1)
    test_n_classen = []
    for p_class, n_class, n_train, n_val in zip(p_classen, n_classen, train_n_classen, val_n_classen):
        if n_class-n_train-n_val > 0:
            test_n_classen.append(n_class-n_train-n_val)
        else:
            test_n_classen.append(1)
            n_train -= 1

    n_dic = \
        {
            train_n: train_n_classen,
            val_n: val_n_classen,
            test_n: test_n_classen,
        }
    #TODO: funktioniert nicht
    return n_dic

def __add_split(data):
    '''die Funktion fügt jedem Datenpunkt einem Split (train/val/test) hinzu
    Args:
        data: (Json List,dic) 
    '''
    # The split must be random and include all classes equaly in all parts
    sorted_data = dict.fromkeys(unique([d.get("Aufgabentyp") for d in data]), []) # sorted_data erstellen mit {"Aufgabentpy1": ["text1", "text2"], "Aufgabentyp2", [text3, text4]}
    for datenpunkt in data:
        sorted_data[datenpunkt["Aufgabentyp"]].append(datenpunkt["Text"])
    
    [random.shuffle(liste) for liste in sorted_data.values()]   #zufällig

    __verhaeltnisse2anzahl(sorted_data)
    #TODO: weiter anpassen
    #Verhältniss der Klassen in einem Split gleichhalten
'''
    for dic in data[:18]:
        dic["split"] = "train"
    for dic in data[18:21]:
        dic["split"] = "val"
    for dic in data[21:]:
        dic["split"] = "test"
'''
    # TODO: die Aufteilung muss ganz zufällig sein
    # TODO: Die Vehältnisse zwischen test/val/train müssen übergeben werden
    # Hyperparameter benutzen

def create_dataset():
    PATH = globale_variablen.get("path_to_data")
    with open(PATH, "r") as file:
        json_data = json.loads(file.read())

    __add_split(json_data)
    dataset = aufgabenDataset.load_dataset_and_make_vectorizer(json_data)

    return dataset


if __name__=="__main__":
    data = \
        {
            "k1": [0, 1, 2, 3, 4, 3, 4, 5],
            "k2": [3, 4, 5, 6, 4, 5, 6],
            "k3": [7, 8, 9, 10, 34, 4, 4]
        }
    
    dic = __verhaeltnisse2anzahl(data)

    print(dic)