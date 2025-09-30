import torch
from saitorch.nn.activations import Sigmoid,Softmax,RELU
from saitorch.nn.loss import CrossEntropyLoss


def test_sigmoid():
    model = Sigmoid()
    x = torch.tensor([0.0, 2.0, -2.0])
    y = model(x)
    model2 = torch.nn.Sigmoid()
    ref = model2(x)
    assert(torch.allclose(y, ref, atol=1e-6))

def test_softmax():
    model = Softmax(dim=0)
    x = torch.tensor([[0.0, 2.0, -2.0],[1.0,2.0,9.0]])
    y = model(x)
    model2 = torch.nn.Softmax(dim=0)
    ref = model2(x)
    assert(torch.allclose(y, ref, atol=1e-6))

def test_relu():
    model = RELU()
    x = torch.tensor([[0.0, 2.0, -2.0],[1.0,2.0,9.0]])
    y = model(x)
    model2 = torch.nn.ReLU()
    ref = model2(x)
    assert(torch.allclose(y, ref, atol=1e-6))


def test_cross_entropy():
    criterion = CrossEntropyLoss(reduction="mean",ignore_index=-100)
    criterion2 = torch.nn.CrossEntropyLoss(reduction="mean",ignore_index=-100)
    loss = criterion(torch.tensor([[0.3,0.8,0.9],[0.3,0.2,0.2]]),torch.tensor([2,1]))
    loss2 = criterion2(torch.tensor([[0.3,0.8,0.9],[0.3,0.2,0.2]]),torch.tensor([2,1]))
    assert(torch.allclose(loss, loss2, atol=1e-6))
