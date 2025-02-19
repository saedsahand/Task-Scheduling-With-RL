
import torch.nn as nn
import torch.nn.functional as F
import torch as th
import numpy as np

def init_weights(m):
        if type(m) == nn.Linear or type(m) == nn.Conv2d:
            th.nn.init.xavier_uniform(m.weight)
            m.bias.data.fill_(0.01)

class DQNAgent(nn.Module):
    '''
        Virtual Done Agent: Assume the req has been placed
        TODO: regularize the virtual done(i.e. negative input to -1 to indicate not appliable)
    '''
    def __init__(self, state_space, act_space, args):
        super(DQNAgent, self).__init__()
        self.obs_space, self.feat_space = state_space[0], state_space[1]
        self.num_actions = act_space

        self.flat = nn.Sequential(
            nn.Flatten(),
        )

        self.fc0 = nn.Sequential(
            nn.Linear(args.N * 4+8, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU()
        )

        self.fc1 = nn.Sequential(
            nn.Linear(256, 256),
            nn.ReLU(),
        )

        self.fc2 = nn.Sequential(
            nn.Linear(256, self.obs_space[0]*2),
            nn.ReLU(),
        )

        self.value = nn.Linear(self.obs_space[0]*2, 1)
        self.adv = nn.Linear(self.obs_space[0]*2, self.num_actions)




    def forward(self, state):
        obs, feat = state[0], state[1]
        h01, h11 = self.flat(obs), self.flat(feat)
        h = th.cat([h01, h11], dim = -1)

        h= self.fc0(h)

        h3 = self.fc1(h)
        h3 = self.fc2(h3)

        adv = self.adv(h3)
        value = self.value(h3)
        q_values = value + adv - th.mean(adv, dim=1, keepdim=True)
        if len(q_values.shape) == 1:
            return q_values.reshape(1, -1)
        else:
            return q_values



class DeltaQAgent(nn.Module):
    '''
        Virtual Done Agent: Assume the req has been placed
        TODO: regularize the virtual done(i.e. negative input to -1 to indicate not appliable)
    '''
    def __init__(self, state_space, act_space, args):
        super(DeltaQAgent, self).__init__()
        self.obs_space, self.feat_space = state_space[0], state_space[1]
        self.num_actions = act_space

        self.flat = nn.Sequential(
            nn.Flatten(),
        )

        self.fc0 = nn.Sequential(
            nn.Linear(4+8, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU()
        )

        self.fc2 = nn.Sequential(
            nn.Linear(64, self.obs_space[0]*2),
            nn.ReLU(),
        )

        self.value = nn.Linear(self.obs_space[0]*2, 1)
        self.adv = nn.Linear(self.obs_space[0]*2, self.num_actions)




    def forward(self, state):
        obs, feat = state[0], state[1]
        h01, h11 = self.flat(obs), self.flat(feat)
        h = th.cat([h01, h11], dim = -1)

        h= self.fc0(h)

        h3 = self.fc1(h)
        h3 = self.fc2(h3)

        adv = self.adv(h3)
        value = self.value(h3)
        q_values = value + adv - th.mean(adv, dim=1, keepdim=True)
        if len(q_values.shape) == 1:
            return q_values.reshape(1, -1)
        else:
            return q_values

