import torch
from torch import nn
from torch.optim import SGD as TorchSGD
from saitorch.optim import SGD


torch.manual_seed(0)

model1 = nn.Linear(4, 3)
model2 = nn.Linear(4, 3)

model2.load_state_dict(model1.state_dict()) 

x = torch.randn(5, 4)
y = torch.tensor([0, 1, 2, 1, 0])

criterion = nn.CrossEntropyLoss()


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

