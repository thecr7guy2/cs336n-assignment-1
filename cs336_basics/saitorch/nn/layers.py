from torch.nn import Module
from torch.nn import Parameter
import torch

class Linear(Module):
    """
    Still Need to undertsnad how to use device and dtype
    """
    def __init__(self,in_features, out_features, device=None, dtype=None):
        super(Linear, self).__init__()
     
        self.weight = Parameter(torch.empty(out_features,in_features),requires_grad=True)
        self.reset_parameters()
    
    def reset_parameters(self) -> None:
        torch.nn.init.trunc_normal_(self.weight, mean=0.0, std=1.0, a=-2.0, b=2.0, generator=None)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
            x = x.matmul(self.weight.t())
            return x
