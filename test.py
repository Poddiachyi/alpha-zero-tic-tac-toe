from agents.random import RandomAgent
from env.game import Game
from nn_wrapper import NNWrapper
from agents.mcts import MCTS, Node
import torch
import os



def main():

    pieces = {1: 'X', 0: 'Draw', -1: 'O'}
    stats = {1: 0, 0: 0, -1: 0}
    bot_stats = {1: 0, 0: 0 }  # 1 is alphazero, 0 is random
    bot_names = {1: 'AlphaZero', 0: 'RandomAgent'}

    for i in range(1000):
        print('Game {} begins'.format(i))
        env = Game(board_size=3)
        net = NNWrapper(env)
        net.net = torch.load(os.path.join('./models/', '{}.pt'.format('current')))
        mcts = MCTS(net)

        node = Node()

        random_agent = RandomAgent(env.get_action_size())

        state, current_player = env.reset()
        while True:
            # env.render()

            if i % 2 == 0:  # random playes as X, alphazerp playes as 0
                if env.current_player == 1:
                    best_child = Node()
                    action = random_agent.act(env.board, env.get_valid_moves())
                    best_child.action = action
                else:
                    best_child = mcts.search(env, node, 0.0001)
                    action = best_child.action
            else:
                if env.current_player == 1:
                    best_child = mcts.search(env, node, 0.0001)
                    action = best_child.action
                else:
                    best_child = Node()
                    action = random_agent.act(env.board, env.get_valid_moves())
                    best_child.action = action

            state, current_player, done = env.step(action)

            best_child.parent = None
            node = best_child  # Make the child node the root node.

            if done:
                winner = env.winner
                if i % 2 == 0:
                    if winner == -1:
                        bot_stats[0] += 1
                    elif winner == 1:
                        bot_stats[1] += 1
                else:
                    if winner == 1:
                        bot_stats[0] += 1
                    elif winner == -1:
                        bot_stats[1] += 1
                break
        # env.render()


    print({bot_names[key]: bot_stats[key] for key in bot_stats})



if __name__ == '__main__':
    main()
