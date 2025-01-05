

import threading

from Game.Ball import Ball
from Game.Player import Player

from math import cos
from time import sleep

from WebApp.views import searchUser


class Game:
    def __init__(self):
        self.playerOne = Player()
        self.playerTwo = Player()
        self.ball = Ball()
        self.playing = False
        self.running = True

    def __del__(self):
        self.playing = False


class GameLoop(threading.Thread):
    def __init__(self):
        super().__init__()
        self.game = Game()


    def run(self):

        while self.game.running:
            if self.game.playing:
                self.game.ball.lock.acquire()
                self.game.playerOne.lock.acquire()
                self.game.playerTwo.lock.acquire()
                ## locks ^
                self.game.ball.tick()
                if cos(self.game.ball.direction) < 0:
                    if self.game.ball.xPos <= 2:
                        if not self.game.ball.check_collision_x_axis(self.game.playerOne.yPos):
                            self.game.ball.reset_coordinates_and_speed()
                            self.game.playerTwo.score += 1
                else:
                    if 198 <= self.game.ball.xPos:
                        if not self.game.ball.check_collision_x_axis(self.game.playerTwo.yPos):
                            self.game.ball.reset_coordinates_and_speed()
                            self.game.playerOne.score += 1
                self.game.ball.check_collisions_y_axis()
                ## locks v
                self.game.ball.lock.release()
                self.game.playerOne.lock.release()
                self.game.playerTwo.lock.release()

            sleep(0.01)


class GameInstance:
    def __init__(self, p1=None, p2=None, p1Name='Plyer One', p2Name='Plyer Two'):
        self.loop = GameLoop()
        self.loop.start()
        if p1 and p2:
            self.playerOne = p1
            self.playerTwo = p2
        if p1Name:
            self.playerOneName = p1Name
        if p2Name:
            self.playerTwoName = p2Name

    def __del__(self):
        self.loop.game.running = False
        self.loop.join()

gameInstance = GameInstance() # this one is for coop

activeGames = {}