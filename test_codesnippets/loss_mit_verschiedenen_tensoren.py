from numpy import float64
import torch
import torch.nn as nn


loss = nn.CrossEntropyLoss()

# batchsize: 2, Klassen:4
y_pred = torch.Tensor([[1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
y_pred.requires_grad_()
y_data = torch.arange(5)
output = loss(y_pred, y_data)
print(output)