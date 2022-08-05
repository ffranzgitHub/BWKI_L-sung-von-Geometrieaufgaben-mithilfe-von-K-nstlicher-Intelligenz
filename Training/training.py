from globale_Variablen import globale_variablen
from Netz.model import AufgabenDetector
from Daten_Laden.text_to_minibatches import generate_batches
from Daten_Laden.data import create_dataset


dataset = create_dataset()
#[x] TODO: Länge des one-hot-encodeten Vectors -> len(Vocabulary)
input_size = len(dataset.get_vectorizer().aufgabe_vocab) 
hidden_size = globale_variablen.get("hidden_size")
num_classes = len(dataset.get_vectorizer().class_vocab) 

NUM_EPOCHS = globale_variablen.get("num_epoches")

model = AufgabenDetector(input_size, hidden_size, num_classes)

model.train()
    
for epoch_i in range(NUM_EPOCHS):
    batches = generate_batches(dataset, globale_variablen.get("batch_size"))
    for batch_i in batches: 
        #TODO: Trainingsloop vervollständigen
        
        #1 Daten laden  
        output = model(batch_i["x_data"])   #TODO: output zu Klassenindizes(int) casten

        #2 Gradienten zurücksetzen

        #3 output berechnen (Forwardpass durchs Netz)

        #4 Loss berechnen

        #5 Gradienten berechnen (Backward pass)

        #6 Optimisieren

