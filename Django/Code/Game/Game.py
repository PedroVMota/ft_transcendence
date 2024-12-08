

from Game import Ball
from Game import Player

class Game:
    def __init__(self):
        self.playerOne = Player.Player()
        self.playerTwo = Player.Player()
        self.ball = Ball.Ball()

gameInstance = Game()