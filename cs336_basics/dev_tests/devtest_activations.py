import torch
from saitorch.nn.activations import Sigmoid,Softmax,RELU

def test_sigmoid():
    model = Sigmoid()
    x = torch.tensor([0.0, 2.0, -2.0])
    y = model(x)
    model2 = torch.nn.Sigmoid()
    ref = model2(x)
    assert(torch.allclose(y, ref, atol=1e-6))

def test_softmax():
    model = Softmax(dim=1)
    x = torch.tensor([[0.0, 2.0, -2.0],[1.0,2.0,9.0]])
    y = model(x)
    model2 = torch.nn.Softmax(dim=1)
    ref = model2(x)
    assert(torch.allclose(y, ref, atol=1e-6))

def test_relu():
    model = RELU()
    x = torch.tensor([[0.0, 2.0, -2.0],[1.0,2.0,9.0]])
    y = model(x)
    model2 = torch.nn.ReLU()
    ref = model2(x)
    assert(torch.allclose(y, ref, atol=1e-6))