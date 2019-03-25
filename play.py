from agents.mcts import MCTS, Node

class HumanPlay(object):

    def __init__(self, game, net):
        self.game = game
        self.net = net

    def play(self):
        print("Start Human vs AI\n")

        mcts = MCTS(self.net)
        game = self.game.clone()  # Create a fresh clone for each game.
        is_done = False
        node = Node()

        print("Enter your move in the form: row, column. Eg: 1,1")
        go_first = input("Do you want to go first: y/n?")

        if go_first.lower().strip() == 'y':
            print("You play as X")
            human_value = 1

            game.render()
        else:
            print("You play as O")
            human_value = -1

        # Keep playing until the game is in a terminal state.
        while not is_done:
            # MCTS simulations to get the best child node.
            # If player_to_eval is 1 play as the Human.
            # Else play as the AI.
            if game.current_player == human_value:
                action = input("Enter your move: ")
                if isinstance(action, str):
                    action = action.split(',')
                    action = game.board_size * int(action[0]) + int(action[1])

                best_child = Node()
                best_child.action = action
            else:
                best_child = mcts.search(game, node, 0.0001)

            action = best_child.action
            self.board, self.current_player, is_done = game.step(action)  # Play the child node's action.

            game.render()

            best_child.parent = None
            node = best_child  # Make the child node the root node.


        if human_value == game.winner:
            print('You won!')
        elif human_value == -game.winner:
            print('You lost.')
        else:
            print('Draw Match')
        print("\n")
