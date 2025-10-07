from torch.optim import Optimizer
import torch

class SGD(Optimizer):
    """Optimizer base class wraps all the init stuff into two things params and defaults.
    The base class also then wraps params into param_groups which can later be used in step/"""
    def __init__(self,params,lr=0.001,momentum=0,weight_decay=0):
        
        if lr <= 0.0:
            raise ValueError(f"Invalid learning rate: {lr}")
        if momentum < 0.0:
            raise ValueError(f"Invalid momentum value: {momentum}")
        if weight_decay < 0.0:
            raise ValueError(f"Invalid weight_decay value: {weight_decay}")
        
        defaults = dict(
            lr=lr,
            momentum=momentum,
            weight_decay=weight_decay,
        )

        super(SGD, self).__init__(params,defaults)

    @torch.no_grad()
    def step(self):
        """
        Simple SGD -> Depends on the dataloader 
            - Can be GD if batch_size = dataset_size
            - Can be SGD if batch_size = 1
            - Can be minibatch-SGD if 1 < batch_size < dataset_size

        Updates params -> Weights and biases

        Theta t1+1 = Theta t - learning_rate * (gradients)

        if weight_decay:
            Theta t+1 = Theta t - learning_rate * ((weight_decay* Theta t) + gradients)
        """

        for i in self.param_groups:
            params = i["params"]
            weight_decay = i["weight_decay"]
            momentum = i["momentum"]
            lr= i ["lr"]
            for param in params:
                if param.grad is None:
                    continue
                gr = torch.clone(param.grad).detach()
                if weight_decay != 0:
                    # "Theta t+1 = Theta t - learning_rate * ((weight_decay* Theta t) + gradients)"
                    gr = gr.add(param,alpha=weight_decay)
                
                if momentum !=0 :
                    # "Here we make use of the state of optimizer already used by the base optimizers class to get the mometum buffer"
                    state = self.state[param]
                    mom_buffer = state.get("momentum_buffer")
                    if mom_buffer is None:
                    ### If the momentum buffer is empty, ie the first gradient isnt there in the buffer
                        # Since we dont want to disturb the gradient terms copy it and then add it the buffer
                        mom_buffer = torch.clone(gr).detach()
                        state["momentum_buffer"] = mom_buffer
                    else:
                        ### beta*(mometum_buffer) + (1-B)gradient
                        mom_buffer.mul_(momentum).add_(gr,alpha=1)
                    gr = mom_buffer
                
                param.add_(gr,alpha=-lr)