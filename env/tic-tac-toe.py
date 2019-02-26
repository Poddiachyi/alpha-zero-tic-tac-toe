class Play(object):

    def __init__(self, agent):
        super().__init__()
        self.winner = None
        self.agent = agent

    def select_square(self):
        """Starts the game with square selection"""
        self.switch = True                              # initializes the switch for the while loop to True
        self.turn = ["X", "O"]                          # turn is either an "X" or an "O"
        self.counter = 0                                # set counter for a possible Tie game - (no winner)
        while self.switch:                              # starts the while loop
            for move in range(2):                       # alternate between "X" and "O"
                self.move = move
                self.get_input(self.turn, self.move)    # calls the get_input function
                if not self.switch:                     # checks to see if the while loop switch has been set to False
                    break                               # if it has, break out of the while loop - end game
                else:
                    self.counter += 1
                if self.counter == 16:                  # if 16 moves have been made with no winner
                    self.switch = False                 # set while loop switch to False
                    self.winner = 'Draw'
                    break
                else:
                    continue
        return self.winner

    def get_input(self, turn, move):
        """Gets input from user"""
        self.turn = turn
        self.move = move
        try:
            action = self.agent.act(self.board)
            self.draw(action, self.turn[move])                          # if no errors, draw the grid, call the draw function
            if self.check_win(self.turn, move):                         # Check if move is a win, call the check_win function
                self.print_win(self.turn, move)                         # if win, print win message, call the print_win function
        except ValueError:
            print("\nError: Please enter a number between 1-16\n")      # print message if a letter is entered
            self.draw_env()                                                 # Draw the board and square numbers again, calls the draw_env function
            self.get_input(self.turn, self.move)                        # try to get input again, call the get_input function


    def check_win(self, turn, move):
        """Checks the ten possibilites for a win"""
        if (self.board[0] == self.turn[move] and self.board[1] == self.turn[move] \
              and self.board[2] == self.turn[move] and self.board[3] == self.turn[move]):
            return True
        elif (self.board[4] == self.turn[move] and self.board[5] == self.turn[move] \
              and self.board[6] == self.turn[move] and self.board[7] == self.turn[move]):
            return True
        elif (self.board[8] == self.turn[move] and self.board[9] == self.turn[move] \
              and self.board[10] == self.turn[move] and self.board[11] == self.turn[move]):
            return True
        elif (self.board[12] == self.turn[move] and self.board[13] == self.turn[move] \
              and self.board[14] == self.turn[move] and self.board[15] == self.turn[move]):
            return True
        elif (self.board[0] == self.turn[move] and self.board[4] == self.turn[move] \
              and self.board[8] == self.turn[move] and self.board[12] == self.turn[move]):
            return True
        elif (self.board[1] == self.turn[move] and self.board[5] == self.turn[move] \
              and self.board[9] == self.turn[move] and self.board[13] == self.turn[move]):
            return True
        elif (self.board[2] == self.turn[move] and self.board[6] == self.turn[move] \
              and self.board[10] == self.turn[move] and self.board[14] == self.turn[move]):
            return True
        elif (self.board[3] == self.turn[move] and self.board[7] == self.turn[move] \
              and self.board[11] == self.turn[move] and self.board[15] == self.turn[move]):
            return True
        elif (self.board[0] == self.turn[move] and self.board[5] == self.turn[move] \
              and self.board[10] == self.turn[move] and self.board[15] == self.turn[move]):
            return True
        elif (self.board[3] == self.turn[move] and self.board[6] == self.turn[move] \
              and self.board[9] == self.turn[move] and self.board[12] == self.turn[move]):
            return True
        else:
            return False

    def print_win(self, turn, move):
        """Prints the winning message"""
        # print(turn[move] + " Wins! \n")
        self.switch = False                     # sets the looping switch in select_square function to False
        self.winner = turn[move]


if __name__ == '__main__':

    stats = {'X': 0, 'O': 0, 'Draw': 0 }

    for _ in range(10000):
        b1 = Play(RandomAgent())

        # b1.draw_env()
        winner = b1.select_square()          # Start the game by calling the select_square function in the Play class
        stats[winner] += 1

    print(stats)
