import torch

def sigmoid(x:torch.Tensor) -> torch.Tensor:
    return 1 /(1 + torch.exp(-x))

def softmax(x:torch.Tensor, dim) -> torch.tensor:
    shift  = torch.max(x,dim=dim,keepdim=True).values
    num = torch.exp(x - shift)
    den = torch.sum(num,dim=dim,keepdim=True)
    return num/den

def logsoftmax(x: torch.Tensor,dim: int) -> torch.Tensor:
    torch.log(softmax(x,dim=dim))

def relu (x:torch.Tensor) -> torch.Tensor:
    return torch.maximum(x,torch.tensor(0.0))

def swiglu (x:torch.Tensor) -> torch.Tensor:
    pass

def gelu(x:torch.Tensor) -> torch.Tensor:
    pass

def tanh(x:torch.Tensor) -> torch.Tensor:
    pass