import torch
from cs336_basics.saitorch.nn.layers import Linear,Embedding

def test_linear():
    in_features, out_features = 4, 3

    my_linear = Linear(in_features, out_features)
    # No Bias since assignment specifically asked me not to have bias
    torch_linear = torch.nn.Linear(in_features, out_features, bias=False)
    state_dict_temp = {"weight":my_linear.weight}
    torch_linear.load_state_dict(state_dict_temp)
    #Same weights to verify.
    x = torch.randn(2, in_features)
    y1 = my_linear(x)
    y2 = torch_linear(x)

    assert torch.allclose(y1, y2, atol=1e-6)

def test_embeddings():
    vocab_length, dimensions = 50304,768
    my_wte = Embedding(vocab_length, dimensions)
    wte = torch.nn.Embedding(vocab_length, dimensions)
    state_dict_temp = {"weight":my_wte.weight}
    wte.load_state_dict(state_dict_temp)
    #Same weights to verify.
    x = torch.randint(0, vocab_length, (2,)) 
    y1 = my_wte(x)
    y2 = wte(x)
    assert torch.allclose(y1, y2, atol=1e-6)

