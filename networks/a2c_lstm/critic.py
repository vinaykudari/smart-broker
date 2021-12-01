import torch
import torch.nn as nn
import torch.nn.functional as F


class CriticLSTM(nn.Module):
    def __init__(self, state_dim, hidden_dim=10, n_layers=2):
        super().__init__()
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
        self.hidden_dim = hidden_dim
        self.input_dim = state_dim
        self.n_layers = n_layers
        self.lstm = nn.LSTM(
            input_size=state_dim,
            hidden_size=hidden_dim,
            num_layers=n_layers,
            dropout=0.2,
            batch_first=True,
        )
        self.fc1 = nn.Linear(hidden_dim, 128)
        self.out = nn.Linear(128, 1)

    def forward(self, x, prev_state):
        x = x.view(1, 1, self.input_dim)
        x, state = self.lstm(x, prev_state)
        x = x.view(1, -1)
        x = F.relu(self.fc1(x))
        out = self.out(x)

        return out, state

    def init_states(self, size):
        hdn_st = torch.zeros(
            self.n_layers,
            size,
            self.hidden_dim,
            requires_grad=False,
        )
        cell_st = torch.zeros(
            self.n_layers,
            size,
            self.hidden_dim,
            requires_grad=False,
        )

        return hdn_st, cell_st