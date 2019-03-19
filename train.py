from arena import Arena
from nn_wrapper import NNWrapper
from agents.mcts import MCTS, Node
from copy import deepcopy

class Train(object):

    def __init__(self, game, net):
        self.game = game
        self.net = net
        self.old_net = NNWrapper(game)  # random

    def train(self, n_iterations=10, n_games=10, n_eval_games=50, threshold=0.6):
        for i in range(n_iterations):
            print('Iteration', i)

            train_set = []

            for j in range(n_games):
                print('Game', j)
                game = self.game.clone()
                self.play_out(game, train_set)

            self.net.save_model()
            self.old_net.load_model()

            self.net.train(train_set, learning_rate=0.001, epochs=10)

            new_mcts = MCTS(self.net)
            old_mcts = MCTS(self.old_net)

            arena = Arena(game, old_mcts, new_mcts)

            win_rate = arena.fight(n_eval_games)
            print('Win rate:', win_rate)

            if win_rate > threshold:
                print('New best model')
                self.net.save_model()
            else:
                print('Leaving old model')
                self.net.load_model()

    def play_out(self, game, train_set):
        mcts = MCTS(self.net)

        is_done = False
        winner = 0
        temp_train_set = []

        root = Node()

        while not is_done:
            best_child = mcts.search(game, root, temperature=0.0001) # very little exploration

            temp_train_set.append([game.get_canonical_board(),  # can a variable passed by reference be changed while in a list
                                  deepcopy(best_child.parent.child_psas), 0])

            action = best_child.action
            _, _, is_done = game.step(action)


            # best_child is now a root
            best_child.parent = None
            root = best_child

        winner = game.winner
        for state in temp_train_set:
            state[2] = winner
            self.augment(state, train_set, game.board_size)

    def augment(self, state, train_set, board_size):
        board = state[0]
        pi_canon = state[1].reshape((board_size, board_size))

        for i in range(4):
            train_set.append([np.rot90(board, i),
                                  np.rot90(pi_canon, i).flatten(),
                                  state[2]])

            train_set.append([np.fliplr(np.rot90(board, i)),
                                  np.fliplr(np.rot90(pi_canon, i)).flatten(),
                                  state[2]])
