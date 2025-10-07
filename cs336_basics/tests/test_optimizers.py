import torch
from torch import nn
from torch.optim import SGD as TorchSGD
from torch.optim import RMSprop as TorchRMSProp
from saitorch.optim import SGD, RMSprop
from saitorch.nn.loss import CrossEntropyLoss

torch.manual_seed(0)

model1 = nn.Linear(4, 3)
model2 = nn.Linear(4, 3)

model2.load_state_dict(model1.state_dict()) 

x = torch.randn(5, 4)
y = torch.tensor([0, 1, 2, 1, 0])

criterion = CrossEntropyLoss()

def test_SGD():
    opt1 = SGD(model1.parameters(), lr=0.1, momentum=0.9, weight_decay=1e-2)
    opt2 = TorchSGD(model2.parameters(), lr=0.1, momentum=0.9, weight_decay=1e-2)

    for step in range(5):
        opt1.zero_grad()
        out1 = model1(x)
        loss1 = criterion(out1, y)
        loss1.backward()
        opt1.step()

        opt2.zero_grad()
        out2 = model2(x)
        loss2 = criterion(out2, y)
        loss2.backward()
        opt2.step()

    assert(all(torch.allclose(p1, p2, atol=1e-6)
            for p1, p2 in zip(model1.parameters(), model2.parameters())))


def test_RMSProp():
    opt1 = RMSprop(model1.parameters(), lr=0.01, alpha=0.99, eps=1e-08, weight_decay=0, momentum=0,)
    opt2 = TorchRMSProp(model2.parameters(), lr=0.01, alpha=0.99, eps=1e-08, weight_decay=0, momentum=0,)

    for step in range(5):
        opt1.zero_grad()
        out1 = model1(x)
        loss1 = criterion(out1, y)
        loss1.backward()
        opt1.step()

        opt2.zero_grad()
        out2 = model2(x)
        loss2 = criterion(out2, y)
        loss2.backward()
        opt2.step()
    
    assert(all(torch.allclose(p1, p2, atol=1e-6)
            for p1, p2 in zip(model1.parameters(), model2.parameters())))


