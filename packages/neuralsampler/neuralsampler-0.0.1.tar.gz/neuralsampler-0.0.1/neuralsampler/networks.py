import torch
import torch.nn as nn
import torch.nn.functional as F
from math import pi

class SmallMLP(nn.Module):
    def __init__(self, n_dims, n_out=1, n_hid=200, layer=nn.Linear):
        super(SmallMLP, self).__init__()
        self.net = nn.Sequential(
            layer(n_dims, n_hid),
            nn.SiLU(),
            layer(n_hid, n_hid),
            nn.SiLU(),
            layer(n_hid, n_hid),
            nn.SiLU(),
            layer(n_hid, n_out),
        )

    def forward(self, x):
        out = self.net(x)
        out = out.squeeze()
        return out
