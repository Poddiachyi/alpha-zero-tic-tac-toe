from env.game import Game
from nn_wrapper import NNWrapper
from train import Train



def main():
    game = Game(board_size=3)
    game.render()
    print(game.get_canonical_board())
    net = NNWrapper(game)

    load_model = False
    if load_model:
        # load model here
        pass

    train = Train(game, net)
    train.train()


if __name__ == '__main__':
    main()
