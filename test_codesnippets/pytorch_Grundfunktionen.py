def Training_Code():
    pass
def Daten_holen(): 
    pass
def Gradienten_zurücksetzen():
    pass
def Vorhersage_bestimmen():
    pass
def Verlust_berechnen():
    pass
def Gradienten_bestimmen():
    pass
def Gewichte_mit_Optimizer_anpassen():
    pass
n_epochs = 10
n_batches = 100

for epoche_i in range(n_epochs):
    for batch_i in range(n_batches):
        Daten_holen()
        Gradienten_zurücksetzen()
        Vorhersage_bestimmen()
        Verlust_berechnen()
        Gradienten_bestimmen()
        Gewichte_mit_Optimizer_anpassen()
        