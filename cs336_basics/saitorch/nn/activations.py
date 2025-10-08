from torch.nn import Module
import torch
from ..core.functional import sigmoid,softmax,relu,silu

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

class ReLU(Module):
    def __init__(self):
        super(ReLU, self).__init__()
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = relu(x)
        return x

class SiLU(Module):
    def __init__(self):
        super(SiLU, self).__init__()
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = silu(x)
        return x