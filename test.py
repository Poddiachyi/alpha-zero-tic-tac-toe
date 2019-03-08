from agents.random import RandomAgent
from env.game import Game


def main():

    pieces = {1: 'X', 0: 'Draw', -1: 'O'}
    stats = {1: 0, 0: 0, -1: 0}

    for i in range(3):
        print('Game {} begins'.format(i))
        env = Game()
        players = [RandomAgent(), None, RandomAgent()] # O, none, X
        state, current_player = env.reset()
        env.render()
        while True:
            action = players[current_player + 1].act(state, env.get_valid_moves())
            state, current_player, done = env.step(action)
            env.render()
            if done:
                stats[env.winner] += 1
                break


    print({pieces[key]: stats[key] for key in stats})



if __name__ == '__main__':
    main()