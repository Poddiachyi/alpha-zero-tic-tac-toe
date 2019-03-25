import torch
import torch.nn as nn
import torch.nn.functional as F

class NeuralNet(nn.Module):
    def __init__(self, action_size):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(action_size, 128)
        self.fc2 = nn.Linear(128, 512)
        self.fc3 = nn.Linear(512, 128)
        self.pi = nn.Linear(128, action_size)
        self.v = nn.Linear(128, 1)

    def forward(self, x):
        out = self.fc1(out)
        out = F.relu(out)
        out = self.fc2(out)
        out = F.relu(out)
        out = self.fc3(out)
        pi = self.pi(out)
        v = self.v(out)
        return F.softmax(pi, dim=0), torch.tanh(v)
