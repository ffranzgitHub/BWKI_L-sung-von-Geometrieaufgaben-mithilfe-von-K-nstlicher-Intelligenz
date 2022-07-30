import torch

def describe(x):
    print("Type: {}".format(x.type()))
    print("Shape/Size: {}".format(x.shape))
    print("Values: \n{}".format(x))

x = torch.Tensor([[0,1,2],[3,4,5]])

describe(x)