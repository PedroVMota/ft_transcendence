

import threading

from Game.Ball import Ball
from Game.Player import Player

from math import cos
from time import sleep

class Game:
    def __init__(self):
        self.playerOne = Player()
        self.playerTwo = Player()
        self.ball = Ball()
        self.running = True

    def __del__(self):
        self.running = False


class GameLoop(threading.Thread):
    def __init__(self):
        super().__init__()
        self.game = Game()


    def run(self):

        while self.game.running:
            self.game.ball.lock.acquire()
            self.game.playerOne.lock.acquire()
            self.game.playerTwo.lock.acquire()
            self.game.ball.tick()
            if cos(self.game.ball.direction) < 0:
                if self.game.ball.xPos <= 2 or 98 <= self.game.ball.yPos:
                    if not self.game.ball.check_collision(self.game.playerOne.yPos):
                        self.game.playerTwo.score += 1
            else:
                if self.game.ball.check_collision(self.game.playerTwo.yPos):
                    if not self.game.ball.check_collision(self.game.playerTwo.yPos):
                        self.game.playerOne.score += 1
            self.game.ball.lock.release()
            self.game.playerOne.lock.release()
            self.game.playerTwo.lock.release()

            sleep(1)


class GameInstance:
    def __init__(self):
        self.loop = GameLoop()
        self.loop.start()

    def __del__(self):
        self.loop.game.running = False
        self.loop.join()

gameInstance = GameInstance()