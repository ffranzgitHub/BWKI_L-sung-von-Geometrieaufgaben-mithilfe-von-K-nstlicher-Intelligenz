from globale_Variablen import globale_variablen

from Netz.model import AufgabenDetector
from Daten_Laden.load_data import load_data

#TODO: Länge des one-hot-encodeten Vectors -> len(Vocabulary)
input_size = 97 # Das habe ich durch testen herausgefunden. TODO Wir sollten aber auf jeden Fall herauskriegen, wie wir das ganze automatisch berechnen können
hidden_size = globale_variablen.get("hidden_size")
num_classes = 2 # TODO siehe input_size, len(class_Vocabulary)

NUM_EPOCHS = globale_variablen.get("num_epoches")

model = AufgabenDetector(input_size, hidden_size, num_classes)

model.train()
    
for epoch_i in range(NUM_EPOCHS):
    batches = load_data()
    for batch_i in batches: 
        #TODO: Trainingsloop vervollständigen
        
        #1 Daten laden  
        output = model(batch_i["x_data"])

        #2 Gradienten zurücksetzen

        #3 output berechnen (Forwardpass durchs Netz)

        #4 Loss berechnen

        #5 Gradienten berechnen (Backward pass)

        #6 Optimisieren

