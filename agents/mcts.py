import numpy as np
from copy import deepcopy

class Node(object):
    def __init__(self, parent=None, action=None, psa=0.0, child_psas=[]):
        self.Nsa = 0
        self.Wsa = 0.0
        self.Qsa = 0.0
        self.Psa = psa
        self.action = action
        self.children = []
        self.child_psas = child_psas
        self.parent = parent

    def is_not_leaf(self):
        if len(self.children) > 0:
            return True
        return False

    def select(self, c_puct=1):
        u_max = 0
        idx_max = 0

        # we select child with max Q + U value
        for idx, child in enumerate(self.children):
            u = child.Qsa + child.Psa * c_puct * np.sqrt(self.Nsa) / (1 + child.Nsa)
            if u > u_max:
                u_max = u
                idx_max = idx
        return self.children[idx_max]

    def expand(self, game, pi):
        # pi is a probability vector for each move in a state
        self.child_psas = deepcopy(pi)
        valid_moves = game.get_valid_moves()
        for i in range(len(valid_moves)):
            if valid_moves[i]:
                self.add_child(parent=self, action=i, pi=pi[i])

    def add_child(self, parent, action, pi=0.):
        node = Node(parent, action, pi)
        self.children.append(node)

    def backprop(self, v):
        self.Nsa += 1
        self.Wsa += v
        self.Qsa = self.Wsa / self.Nsa

    def show(self):
        print('action', self.action)
        print('children', self.children)
        print('child_psas', self.child_psas)
        print('parent', self.parent)
        print()

class MCTS(object):

    def __init__(self, net):
        self.root = None
        self.game = None
        self.net = net

    def search(self, game, node, temperature=1, n_sims=50):
        self.root = node
        self.game = game

        for i in range(n_sims):
            node_temp = self.root
            game_temp = self.game.clone()

            while node_temp.is_not_leaf():
                node_temp = node_temp.select()
                game_temp.step(node_temp.action)

            pi, v = self.net.predict(game_temp.get_canonical_board())
            # game_temp.render()
            # print(v)
            # print(pi)

            pi = pi.cpu().numpy()

            if node_temp.parent is None:
                pi = self.add_dirichlet_noise(game_temp, pi)


            valid_moves = game_temp.get_valid_moves()
            pi = pi * valid_moves

            pi_sum = pi.sum()
            if pi_sum > 0:
                pi /= pi_sum

            node_temp.expand(game_temp, pi)

            while node_temp is not None:
                node_temp.backprop(v)
                node_temp = node_temp.parent

        u_max = 0
        idx_max = 0

        # Select the child's move using a temperature parameter.
        for idx, child in enumerate(self.root.children):
            temperature_exponent = int(1 / temperature)

            if child.Nsa ** temperature_exponent > u_max:
                u_max = child.Nsa ** temperature_exponent
                idx_max = idx

        return self.root.children[idx_max]


    def add_dirichlet_noise(self, game, psa_vector):
        dirichlet_alpha = 0.5
        epsilon = 0.25
        dirichlet_input = [dirichlet_alpha for x in range(game.get_action_size())]

        dirichlet_list = np.random.dirichlet(dirichlet_input)
        noisy_psa_vector = []

        for idx, psa in enumerate(psa_vector):
            noisy_psa_vector.append(
                (1 - epsilon) * psa + epsilon * dirichlet_list[idx])

        return np.array(noisy_psa_vector)
