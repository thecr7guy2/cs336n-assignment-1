from torch.optim import Optimizer
import torch

class Adam(Optimizer):
    """Optimizer base class wraps all the init stuff into two things params and defaults.
    The base class also then wraps params into param_groups which can later be used in step/"""
    def __init__(self,params,lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0):
        
        if lr <= 0.0:
            raise ValueError(f"Invalid learning rate: {lr}")
        if weight_decay < 0.0:
            raise ValueError(f"Invalid weight_decay value: {weight_decay}")

        
        defaults = dict(
            lr=lr,
            betas = betas,
            eps = eps,
            weight_decay=weight_decay,
        )

        super(Adam, self).__init__(params,defaults)

    @torch.no_grad()
    def step(self):
        """
        """

        for i in self.param_groups:
            params = i["params"]
            weight_decay = i["weight_decay"]
            betas = i ["betas"]
            eps = i["eps"]
            lr= i ["lr"]
            for param in params:
                if param.grad is None:
                    continue
                gr = torch.clone(param.grad).detach()
                if weight_decay != 0:
                    # "Theta t+1 = Theta t - learning_rate * ((weight_decay* Theta t) + gradients)"
                    gr = gr.add(param,alpha=weight_decay)

                state = self.state[param]
                exp_avg = state.get("exp_avg")
                if exp_avg is None:
                    exp_avg = gr.mul(1-betas[0])
                    state["exp_avg"] = exp_avg
                else:
                    exp_avg.mul_(betas[0]).add_(gr,alpha=(1-betas[0]))
                
                exp_avg_sq = state.get("exp_avg_sq")
                if exp_avg_sq is None:
                    exp_avg_sq = gr.mul(gr)
                    exp_avg_sq.mul_(1-betas[1])
                    state["exp_avg_sq"] = exp_avg_sq
                else:
                    exp_avg_sq.mul_(betas[1]).addcmul_(gr,gr,value=(1-betas[0]))
        



