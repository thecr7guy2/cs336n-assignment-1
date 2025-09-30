from saitorch.nn.loss import CrossEntropyLoss
import torch


def test_cross_entropy():
    criterion = CrossEntropyLoss(reduction="mean",ignore_index=-100)
    criterion2 = torch.nn.CrossEntropyLoss(reduction="mean",ignore_index=-100)
    loss = criterion(torch.tensor([[0.3,0.8,0.9],[0.3,0.2,0.2]]),torch.tensor([2,1]))
    loss2 = criterion2(torch.tensor([[0.3,0.8,0.9],[0.3,0.2,0.2]]),torch.tensor([2,1]))
    assert(torch.allclose(loss, loss2, atol=1e-6))
