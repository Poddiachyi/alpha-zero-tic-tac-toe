from env.game import Game
from nn_wrapper import NNWrapper
from train import Train
from play import HumanPlay
import torch
import os



def main():
    game = Game(board_size=3)
    net = NNWrapper(game)



    # net.net = torch.load(os.path.join('./models/', '{}.pt'.format('current')))
    # human_play = HumanPlay(game, net)
    # human_play.play()

    train = Train(game, net)
    train.train()


if __name__ == '__main__':
    main()
