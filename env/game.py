import numpy as np
from copy import deepcopy

class Game(object):

    def __init__(self, board_size=4):
        self.board_size = board_size
        self.size = board_size * board_size
        self.board = [0] * board_size * board_size
        self.pieces = {1: 'X', 0: ' ', -1: 'O'}
        self.current_player = 1
        self.winner = 0

    def get_action_size(self):
        return self.size

    def get_canonical_board(self):
        canonical_board = np.array(self.board).reshape((self.board_size, self.board_size))
        return canonical_board


    def step(self, action):
        self.board[action] = self.current_player
        done = self._is_done()
        self.current_player = -self.current_player
        return self.board, self.current_player, done


    def reset(self):
        self.board = [0] * self.size
        self.current_player = 1
        self.winner = 0
        return self.board, self.current_player

    def clone(self):
        game = Game()
        game.board = deepcopy(self.board)
        game.current_player = self.current_player
        game.winner = self.winner
        return game

    def _is_done(self):
        value = self.current_player
        for i in range(0, self.size, self.board_size):
            row = self.board[i:i + self.board_size]
            row_set = list(set(row))
            if len(row_set) == 1 and  row_set[0] == value:
                self.winner = self.current_player
                return True

        for i in range(self.board_size):
            column = [self.board[i + j] for j in range(0, self.size, self.board_size)]
            column_set = list(set(column))
            if len(column_set) == 1 and column_set[0] == value:
                self.winner = self.current_player
                return True

        left_digonal = [self.board[j] for j in range(0, self.size, self.board_size + 1)]
        left_digonal_set = list(set(left_digonal))
        if len(left_digonal_set) == 1 and left_digonal_set[0] == value:
            self.winner = self.current_player
            return True

        right_digonal = [self.board[j] for j in range(self.board_size - 1, self.size - self.board_size + 1, self.board_size - 1)]
        right_digonal_set = list(set(right_digonal))
        if len(right_digonal_set) == 1 and right_digonal_set[0] == value:
            self.winner = self.current_player
            return True

        if np.count_nonzero(self.board) == self.size:
            self.winner = 0
            return True

        return False

    def get_valid_moves(self):
        valids = np.array([0. if val == 1 or val == -1 else 1. for val in self.board])
        return valids


    def render(self):
        x = "-"
        y = "|"
        z = "  "
        w = ' '
        spaces = 5
        print(z * spaces, x * (self.board_size * 4 - 1))
        for i in range(0, self.size, self.board_size):
            row_print = z * spaces + y + w
            row = [self.pieces[piece] for piece in self.board[i:i + self.board_size]]
            for val in row:
                row_print += val + w
                row_print += y + w
            print(row_print)
            print(z * spaces, x * (self.board_size * 4 - 1))
        print()


    def get_symmetries(self):
        pass
