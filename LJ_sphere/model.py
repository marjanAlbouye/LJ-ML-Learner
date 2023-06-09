import torch
import torch.nn as nn

class NN(nn.Module):
    def __init__(self, in_dim,  hidden_dim, out_dim, n_layers, act_fn="ReLU", dropout=0.3, inp_mode="pos"):
        super(NN, self).__init__()
        self.in_dim = in_dim
        self.hidden_dim = hidden_dim
        self.out_dim = out_dim
        self.n_layers = n_layers
        self.act_fn = act_fn
        self.dropout = dropout
        self.inp_mode = inp_mode
        
        if self.inp_mode == "r":
            self.in_dim += 1

        self.net = nn.Sequential(*self._get_net())

    def _get_act_fn(self):
        act = getattr(nn, self.act_fn)
        return act()

    def _get_net(self):
        layers = [nn.Linear(self.in_dim, self.hidden_dim), self._get_act_fn()]
        for i in range(self.n_layers - 1):
            layers.append(nn.Linear(self.hidden_dim, self.hidden_dim))
            # if self.batch_dim:
            #     layers.append(nn.BatchNorm1d(self.batch_dim))
            layers.append(self._get_act_fn())
            layers.append(nn.Dropout(p=self.dropout))
        layers.append(nn.Linear(self.hidden_dim, self.out_dim))
        return layers

    def forward(self, x):
        if self.inp_mode == "r":
            # include center-to-center distance as a feature 
            x = torch.cat((x, torch.norm(x, dim=1, keepdim=True).to(x.device)), dim=1).to(x.device)
        out = self.net(x)
        return out
    
    
class NNGrow(nn.Module):
    def __init__(self, in_dim,  hidden_dim, out_dim, n_layers, act_fn="ReLU", dropout=0.3, inp_mode="pos"):
        super(NNGrow, self).__init__()
        self.in_dim = in_dim
        self.hidden_dim = hidden_dim
        self.out_dim = out_dim
        self.n_layers = n_layers
        self.act_fn = act_fn
        self.dropout = dropout
        self.inp_mode = inp_mode
        
        if self.inp_mode == "r":
            self.in_dim += 1

        self.net = nn.Sequential(*self._get_net())

    def _get_act_fn(self):
        act = getattr(nn, self.act_fn)
        return act()

    def _get_net(self):
        layers = [nn.Linear(self.in_dim, self.hidden_dim[0]), self._get_act_fn()]
        for i in range(1, len(self.hidden_dim)):
            layers.append(nn.Linear(self.hidden_dim[i-1], self.hidden_dim[i]))
            # if self.batch_dim:
            #     layers.append(nn.BatchNorm1d(self.batch_dim))
            layers.append(self._get_act_fn())
            layers.append(nn.Dropout(p=self.dropout))
        layers.append(nn.Linear(self.hidden_dim[-1], self.out_dim))
        return layers

    def forward(self, x):
        if self.inp_mode == "r":
            # include center-to-center distance as a feature 
            x = torch.cat((x, torch.norm(x, dim=1, keepdim=True).to(x.device)), dim=1).to(x.device)
        out = self.net(x)
        return out