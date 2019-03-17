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

    def select(self, c_puct=2):
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
        # p is a probability vector for each move in a state
        self.child_psas = deepcopy(pi)
        valid_moves = game.get_valid_moves()
        for i in valid_moves:
            if valid_moves[i]:
                self.add_child(parent=self, action=i, pi=pi[i])

    def add_child(self, parent, action, pi=0.):
        node = Node(parent, action, pi)
        self.children.append(node)

    def backprop(self, wsa, v):  # do i really need to pass wsa here?
        self.Nsa += 1
        self.Wsa = wsa + v       # it probably must be self.Wsa += v
        self.Qsa = self.Wsa / self.Nsa

class MCTS(object):

    def __init__(self, net):
        self.root = None
        self.game = None
        self.net = net

    def search(self, game, node, temperature=1, n_sims=10):
        self.root = node
        self.game = game   # don't loke naming. game and self.game

        for i in range(n_sims):
            node = self.root
            game = self.game.clone()

            while node.is_not_leaf():
                node = node.select()
                game.step(node.action)

            pi, v = self.net(game.get_canonical_board())

            valid_moves = game.get_valid_moves()
            pi = p * valid_moves

            pi_sum = pi.sum()
            if pi_sum > 0:
                pi /= pi_sum

            node.expand(game, pi)

            wsa = game.winner

            while node is not None:
                wsa = -wsa
                v = -v
                node.back_prop(wsa, v)
                node = node.parent

        u_max = 0
        idx_max = 0

        # Select the child's move using a temperature parameter.
        for idx, child in enumerate(self.root.children):
            temperature_exponent = int(1 / temperature)

            if child.Nsa ** temperature_exponent > highest_nsa:
                highest_nsa = child.Nsa ** temperature_exponent
                highest_index = idx

        return self.root.children[highest_index]
