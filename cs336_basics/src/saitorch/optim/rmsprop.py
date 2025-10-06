from torch.optim import Optimizer
import torch

class RMSprop(Optimizer):
    """Optimizer base class wraps all the init stuff into two things params and defaults.
    The base class also then wraps params into param_groups which can later be used in step/"""
    def __init__(self,params,lr=0.001,alpha=0.99,eps=1e-08,weight_decay=0,momentum=0):
        
        if lr <= 0.0:
            raise ValueError(f"Invalid learning rate: {lr}")
        if momentum < 0.0:
            raise ValueError(f"Invalid momentum value: {momentum}")
        if weight_decay < 0.0:
            raise ValueError(f"Invalid weight_decay value: {weight_decay}")
        if alpha < 0.0:
            raise ValueError(f"Invalid alpha value: {alpha}")
        
        defaults = dict(
            lr=lr,
            momentum=momentum,
            alpha = alpha,
            eps = eps,
            weight_decay=weight_decay,
        )

        super(RMSprop, self).__init__(params,defaults)

    @torch.no_grad()
    def step(self):
        """
        """

        for i in self.param_groups:
            params = i["params"]
            weight_decay = i["weight_decay"]
            momentum = i["momentum"]
            alpha = i["alpha"]
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
                square_avg = state.get("square_avg")
                if square_avg is None:
                    square_avg = gr.mul(gr,alpha=(1-alpha))
                    state["square_avg"] = square_avg
                else:
                    square_avg.mul_(alpha).addcmul_(gr,gr,value=(1-alpha))
                
                if momentum !=0 :
                    mom_buffer = state.get("momentum_buffer")
                    if mom_buffer is None:
                        mom_buffer = gr
                        state["momentum_buffer"] = mom_buffer
                    else:
                        mom_buffer.mul_(momentum).addcdiv_(gr,square_avg.add(eps).sqrt())
                
                    gr = mom_buffer

                    param.add_(mom_buffer,alpha = -lr)
                
                else:
                    param.addcdiv_(gr,square_avg.add(eps).sqrt(),alpha = -lr)
                



