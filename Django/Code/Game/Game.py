

from Game.Ball import Ball
from Game.Player import Player

class Game:
    def __init__(self):
        self.playerOne = Player()
        self.playerTwo = Player()
        self.ball = Ball()


gameInstance = Game()