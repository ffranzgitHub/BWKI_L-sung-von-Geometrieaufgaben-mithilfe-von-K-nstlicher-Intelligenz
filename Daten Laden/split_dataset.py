
def _add_split(data):
    '''die Funktion verändert die Json Variable selbst
    
    Args:
        data: (Json List,dic) 
    '''
    for dic in data[:18]:
        dic["split"] = "train"
    for dic in data[18:21]:
        dic["split"] = "val"
    for dic in data[21:]:
        dic["split"] = "test"

    # TODO: die Aufteilung muss ganz zufällig sein
    # TODO: Die Vehältnisse zwischen test/val/train müssen übergeben werden