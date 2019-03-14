import numpy as np
from copy import deepcopy

class Game(object):

    def __init__(self):
        self.board = [0] * 16
        self.pieces = {1: 'X', 0: ' ', -1: 'O'}
        self.current_player = 1
        self.winner = 0


    def step(self, action):
        self.board[action] = self.current_player
        done = self._is_done()
        self.current_player = -self.current_player
        return self.board, self.current_player, done


    def reset(self):
        self.board = [0] * 16
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
        for i in range(0, 13, 4):
            if self.board[i] == self.board[i+1] == self.board[i+2] == self.board[i+3] == value:
                self.winner = self.current_player
                return True

        for i in range(4):
            if self.board[i] == self.board[i+4] == self.board[i+8] == self.board[i+12] == value:
                self.winner = self.current_player
                return True

        if self.board[0] == self.board[5] == self.board[10] == self.board[15] == value or \
           self.board[3] == self.board[6] == self.board[9] == self.board[12] == value:
            self.winner = self.current_player
            return True


        if np.count_nonzero(self.board) == 16:
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
        board = self.board
        pieces = self.pieces
        print(z * 16, pieces[board[0]], y, pieces[board[1]], y, pieces[board[2]], y, pieces[board[3]])
        print(z * 16, x * 14)
        print(z * 16, pieces[board[4]], y, pieces[board[5]], y, pieces[board[6]], y, pieces[board[7]])
        print(z * 16, x * 14)
        print(z * 16, pieces[board[8]], y, pieces[board[9]], y, pieces[board[10]], y, pieces[board[11]])
        print(z * 16, x * 14)
        print(z * 16, pieces[board[12]], y, pieces[board[13]], y, pieces[board[14]], y, pieces[board[15]])
        print()


    def get_symmetries(self):
        pass
