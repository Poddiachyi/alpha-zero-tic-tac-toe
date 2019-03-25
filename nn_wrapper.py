from agents.resnet import ResNet
from agents.ffn import NeuralNet
import torch
import torch.optim as optim
import os

import numpy as np



class NNWrapper(object):

    def __init__(self, game):
        self.game = game
        self.net = ResNet(layers=[2, 2, 2], action_size=game.get_action_size())

        self.net.cuda()

    def predict(self, board):
        state = torch.FloatTensor(np.array(board).astype(np.float64)).cuda()
        state = state.view(-1, 1, 3, 3)
        self.net.eval()
        with torch.no_grad():
            pi, v = self.net(state)
        return pi[0], v[0]

    def train(self, train_set, learning_rate=0.01, epochs=20, batch_size=512):
        optimizer = optim.Adam(self.net.parameters(), lr=learning_rate)

        for epoch in range(epochs):
            print("Epoch", epoch)

            n_samples = len(train_set)

            for i in range(0, n_samples, batch_size):
                sample_ids = np.random.randint(n_samples, size=batch_size)
                boards, pis, vs = list(zip(*[train_set[i] for i in sample_ids]))

                boards = torch.FloatTensor(np.array(boards).astype(np.float64)).cuda()
                pi_true = torch.FloatTensor(np.array(pis)).cuda()
                v_true = torch.FloatTensor(np.array(vs).astype(np.float64)).cuda()

                state = boards.view(batch_size, 1, 3, 3)
                pi_pred, v_pred = self.net(state)

                loss, v_loss, pi_loss = self.compute_loss(pi_pred, pi_true, v_pred, v_true)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                with open('losses.csv', 'a') as loss_file:
                    loss_file.write('{},{},{}\n'.format(loss, v_loss, pi_loss))



    def compute_loss(self, pi_pred, pi_true, v_pred, v_true):
        v_loss = ((v_true - v_pred) ** 2).mean()
        pi_loss = -(pi_true * pi_pred).mean()
        return v_loss + pi_loss, v_loss, pi_loss


    def save_model(self, filename='current'):
        save_path = './models/'
        torch.save(self.net, os.path.join(save_path, '{}.pt'.format(filename)))

    def load_model(self, filename='current'):
        save_path = './models/'
        self.net = torch.load(os.path.join(save_path, '{}.pt'.format(filename)))
