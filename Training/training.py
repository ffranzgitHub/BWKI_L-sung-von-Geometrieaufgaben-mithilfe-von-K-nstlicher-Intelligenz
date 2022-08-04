import torch
import torch.nn as nn

from Netz.model import AufgabenDetector
from Daten_Laden.load_data import load_data
import numpy as np


input_size = 97 # Das habe ich durch testen herausgefunden. TODO Wir sollten aber auf jeden Fall herauskriegen, wie wir das ganze automatisch berechnen können
hidden_size = 256
num_classes = 2 # TODO siehe input_size

NUM_EPOCHS = 1

model = AufgabenDetector(input_size, hidden_size, num_classes)

model.train()

#batches_numpy = np.fromiter(batches, dtype=np.float32) # TODO das ganze ist noch Fehlerhaft und gibt einen Fehler zurück. Ich weiß aber nicht genau, wie ich diesen Behebn soll
#batches_tensor = torch.from_numpy(batches_numpy, dtype=torch.float32)

    
for epoch_i in range(NUM_EPOCHS):
    batches = load_data()
    for batch_i in batches:        
        test_input = batch_i["x_data"]
        #print(test_input)

        output = model(batch_i["x_data"])

        #TODO: Trainingsloop vervollständigen
        print(output)