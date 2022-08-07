from globale_Variablen import globale_variablen
from Netz.model import AufgabenDetector
from Daten_Laden.text_to_minibatches import generate_batches
from Daten_Laden.data import create_dataset
import torch.nn as nn
import torch


dataset = create_dataset()

#[x] TODO: Länge des one-hot-encodeten Vectors -> len(Vocabulary)
input_size = len(dataset.get_vectorizer().aufgabe_vocab) 
hidden_size = globale_variablen.get("hidden_size")
num_classes = len(dataset.get_vectorizer().class_vocab) 
learning_rate = globale_variablen.get("learning_rate")

NUM_EPOCHS = globale_variablen.get("num_epoches")

model = AufgabenDetector(input_size, hidden_size, num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

model.train()
    
correct_counter = 0 #?
all_counter = 0     #?

for epoch_i in range(NUM_EPOCHS):
    batches = generate_batches(dataset, globale_variablen.get("batch_size"))
    for batch_i in batches: 
        #TODO: Trainingsloop vervollständigen
        
        #1 Daten laden  
        x_data = batch_i["x_data"]
        y_target = batch_i["y_target"]

        #2 output berechnen (Forwardpass durchs Netz)
        output = model(x_data)   #TODO: output zu Klassenindizes(int) casten

        #3 Loss berechnen
        loss = criterion(output, y_target)

        #TODO: print in eine seperate Funktion auslagern?
        if epoch_i % 100 == 0:
            out_idx = torch.argmax(output)
            label_idx = y_target.item()

            all_counter += 1
            result = "Not correct"
            if out_idx == label_idx:
                correct_counter += 1
                result = "Correct"
            print(f"Loss: {loss.item()}     OUT: {out_idx}     LABEL: {label_idx}    CHECK: {result}")

        #4 Gradienten zurücksetzen
        optimizer.zero_grad()

        #5 Gradienten berechnen (Backward pass)
        loss.backward()

        #6 Optimisieren
        optimizer.step()



print(f"{correct_counter}/{all_counter} sind richtig --> {correct_counter/all_counter*100}%")