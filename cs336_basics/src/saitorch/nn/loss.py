from torch.nn import Module
import torch
from ..core.loss import crossentropyloss

class CrossEntropyLoss(Module):
    def __init__(self,reduction="mean",ignore_index=-100):
        super(CrossEntropyLoss, self).__init__()
        self.reduction = reduction
        self.ignore_index = ignore_index
    def forward(self, logits: torch.Tensor,targets:torch.Tensor) -> torch.Tensor:
        loss = crossentropyloss(logits,targets,self.reduction,self.ignore_index)
        return loss