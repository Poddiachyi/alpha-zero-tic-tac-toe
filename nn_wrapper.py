from agents.reset import ResNet
import torch.optim as optim


class NNWrapper(object):

    def __init__(self, game):
        self.game = game
        self.net = ResNet(layers=[2, 2, 2], action_size=game.get_action_size())

    def predict(self, state):
        pi, v = self.net(state)
        return pi[0], v[0]

    def train(self, train_set, learning_rate=0.001, epochs):
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        for epoch in range(epochs):
            print("Epoch", epoch)

            # create batches



    def compute_loss(self, pi_pred, pi_true, v_pred, v_true):
        pass

    def save_model(self, filename):
        pass

    def load_model(self, filename):
        pass
