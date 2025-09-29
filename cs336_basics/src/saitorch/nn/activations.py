from torch.nn import Module
import torch
from ..core.functional import sigmoid,softmax,relu

class Sigmoid(Module):
    def __init__(self):
        super(Sigmoid, self).__init__()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = sigmoid(x)
        return x

class Softmax(Module):
    def __init__(self,dim:int):
        super(Softmax, self).__init__()
        self.dim = dim 
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = softmax(x,self.dim)
        return x

class RELU(Module):
    def __init__(self):
        super(RELU, self).__init__()
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = relu(x)
        return x