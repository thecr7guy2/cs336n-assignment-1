import torch
from .functional import logsoftmax

def negativeloglikelihoodloss(log_probs:torch.Tensor, targets:torch.Tensor,reduction="mean",ignore_index=100) -> torch.Tensor:
    mask = targets != ignore_index
    selected_log_probs = log_probs[torch.arange(targets.shape[0]),targets]
    selected_log_probs = selected_log_probs[mask]
    selected_log_probs = -selected_log_probs
    # This step here is very intelligent since there is only one rights class we just directly choose that
    if reduction == "mean":
        return torch.mean(selected_log_probs)
    
def crossentropyloss(logits:torch.Tensor, targets:torch.Tensor,reduction="mean",ignore_index=100) -> torch.Tensor:
    "Combination of NLL loss and log Softmax"
    log_probs = logsoftmax(logits,dim=1)
    selected_log_probs = negativeloglikelihoodloss(log_probs,targets,reduction,ignore_index)
    if reduction == "mean":
        return torch.mean(selected_log_probs)