import torch
import torch.nn as nn

from Netz.model import AufgabenDetector
from Daten_Laden.text_to_minibatches import generate_batches
from Daten_Laden.split_dataset import _add_split
from Daten_Laden.start_load_data import x, input_size
import numpy as np


input_size = input_size # Das habe ich durch testen herausgefunden. TODO Wir sollten aber auf jeden Fall herauskriegen, wie wir das ganze automatisch berechnen können
hidden_size = 256
num_classes = 2 # TODO siehe input_size

NUM_EPOCHS = 100

model = AufgabenDetector(input_size, hidden_size, num_classes)

model.train()

x_numpy = np.fromiter(x, dtype=np.float32) # TODO das ganze ist noch Fehlerhaft und gibt einen Fehler zurück. Ich weiß aber nicht genau, wie ich diesen Behebn soll
x_tensor = torch.from_numpy(x_numpy, dtype=torch.float32)
print(x_tensor)
    
for i in range(NUM_EPOCHS):
    output = model(x[:]["x_data"])