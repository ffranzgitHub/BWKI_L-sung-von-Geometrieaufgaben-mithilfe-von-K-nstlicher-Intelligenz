import os
from datetime import datetime
from globale_Variablen import globale_variablen
from Netz.model import AufgabenDetector
from Daten_Laden.text_to_minibatches import generate_batches
from Daten_Laden.data import vorverarbeitung_und_dataset
import torch.nn as nn
import torch

# Speichert den aktuellen Fortschritt (Modelparameter, Logs etc.)
def save_current_progress(model:AufgabenDetector, logs:list, training_name:str):
    save_model = model.state_dict()
    save_logs = logs
    dirs = os.listdir(globale_variablen["path_to_progress"]+training_name)
    dirs.insert(0, "-1SAVE.pt") # Damit es min. ein exestierenden Save gibt (auch wenn er leer ist)
    last_save = dirs[-1].split("SAVE")[0]
    # Nimmt an, dass der letzte Ordner der neuste ist

    torch.save({
        "save_model": save_model,
        "save_logs": save_logs,
    }, globale_variablen["path_to_progress"]+f"{training_name}/{int(last_save)+1}SAVE.pt")




# Preprocessing und Dataset
dataset = vorverarbeitung_und_dataset()


input_size = len(dataset.get_vectorizer().aufgabe_vocab)
hidden_size = globale_variablen.get("hidden_size")
num_classes = len(dataset.get_vectorizer().class_vocab)
learning_rate = globale_variablen.get("learning_rate")

NUM_EPOCHS = globale_variablen.get("num_epoches")

model = AufgabenDetector(input_size, hidden_size, num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

model.train()

correct_counter = 0  # Zählt die Batches, die korrekt bestimmt wurden
all_counter = 0     # Zählt die Batches, getestet wurden
# Zusammen wird mit diesen Variablen am Ende geguckt, wie viel Prozent der Traings Batche das Netz
# korrekt im letzen Durchlauf bestimmen konnte

last_logs = []
training_name = str(datetime.now().strftime("%d.%m.%Y.%H.%M.%S"))
os.mkdir(f"{globale_variablen['path_to_progress']}{training_name}")
#os.mkdir(f"{globale_variablen['path_to_progress']}{training_name}/1")
# -1 damit bereits eine 'Epoche' gespeichert ist und max kein Empty Arg bekommt

for epoch_i in range(NUM_EPOCHS):
    batches = generate_batches(dataset, globale_variablen.get("batch_size"))
    for batch_i in batches:
        # TODO: Trainingsloop vervollständigen

        # 1 Daten laden
        x_data = batch_i["x_data"]
        y_target = batch_i["y_target"]

        # 2 output berechnen (Forwardpass durchs Netz)
        output = model(x_data)

        # 3 Loss berechnen
        loss = criterion(output, y_target)

        # TODO: print in eine seperate Funktion auslagern?
        if epoch_i % 100 == 0:
            out_idx = torch.argmax(output)
            label_idx = y_target.item()

            all_counter += 1
            result = "Not correct"
            if out_idx == label_idx:
                correct_counter += 1
                result = "Correct"

            current_log = f"Loss: {loss.item()}     OUT: {out_idx}     LABEL: {label_idx}    CHECK: {result}    EPOCH: {epoch_i}"
            last_logs.append(current_log)
            print(current_log)



        # 4 Gradienten zurücksetzen
        optimizer.zero_grad()

        # 5 Gradienten berechnen (Backward pass)
        loss.backward()

        # 6 Optimisieren
        optimizer.step()


    if epoch_i % 1_000 == 0:
            save_current_progress(model, last_logs, training_name)
            last_logs = []


print(f"{correct_counter}/{all_counter} sind richtig --> {correct_counter/all_counter*100}%")



torch.save(model.state_dict(), globale_variablen["path_to_model"])
