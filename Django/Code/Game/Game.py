

import threading

from Game.Ball import Ball
from Game.Player import Player

from math import cos, tan, fabs, ceil
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


class AILoop(threading.Thread):
    def __init__(self, gameRef):
        super().__init__()
        self.game: Game = gameRef

    def predict_ball_position(self):
        predicted_position = (200 - self.game.ball.xPos) * tan(self.game.ball.direction)

        # print("[predict_ball_position]")
        # print("ball pos: {", self.game.ball.xPos, ",", self.game.ball.yPos, "}")
        # print("ball angle:", self.game.ball.direction)
        # print("predicted pos: ", predicted_position + 50)
        predicted_position += 50

        while predicted_position > 100 or predicted_position < 0:
            if predicted_position > 100:
                predicted_position = 100 - (predicted_position - 100)
            elif  predicted_position < 0:
                predicted_position = fabs(predicted_position)

        print("returning predicted position as:", predicted_position)

        return predicted_position

    def make_ai_moves(self, target_position):
        offset_to_target = self.game.playerOne.yPos - target_position
        number_of_steps = ceil(fabs(offset_to_target) / self.game.playerTwo.speed)
        print("number_of_steps:", number_of_steps)
        original_n_of_steps = number_of_steps
        if number_of_steps <= 0:
            self.game.ball.lock.release()
            self.game.playerTwo.lock.release()
            sleep(1)
            self.game.ball.lock.acquire()
            self.game.playerTwo.lock.acquire()
        else:
            while number_of_steps > 0:
                if offset_to_target < -5:
                    self.game.playerTwo.lock.release()
                    self.game.playerTwo.handle_paddle_movement(1)
                    self.game.playerTwo.lock.acquire()
                elif offset_to_target > 5:
                    self.game.playerTwo.lock.release()
                    self.game.playerTwo.handle_paddle_movement(-1)
                    self.game.playerTwo.lock.acquire()
                number_of_steps -= 1
                self.game.playerTwo.lock.release()
                self.game.ball.lock.release()
                sleep_time = 1 / original_n_of_steps
                print("going to sleep ", sleep_time, " seconds")
                sleep(sleep_time)
                self.game.playerTwo.lock.acquire()
                self.game.ball.lock.acquire()


    def run(self):
        while True:
            sleep(1)
            if self.game.running and self.game.playing:
                self.game.ball.lock.acquire()
                self.game.playerTwo.lock.acquire()
                should_wait = True
                if cos(self.game.ball.direction) > 0:
                    predicted_pos = self.predict_ball_position()
                    self.make_ai_moves(predicted_pos)
                    should_wait = False
                self.game.ball.lock.release()
                self.game.playerTwo.lock.release()
                if should_wait:
                    sleep(1)


class GameInstance:
    def __init__(self, p1=None, p2=None, p1Name='Player One', p2Name='Player Two', aiIncluded=False):
        self.loop = GameLoop()
        self.loop.start()
        self.aiLoop = None
        if p1 and p2:
            self.playerOne = p1
            self.playerTwo = p2
        if p1Name:
            self.playerOneName = p1Name
        if p2Name:
            self.playerTwoName = p2Name
        if aiIncluded:
            self.aiLoop = AILoop(self.loop.game)
            self.aiLoop.start()



    def __del__(self):
        self.loop.game.running = False
        self.loop.join()
        if self.aiLoop is not None:
            self.aiLoop.join()


gameInstance = GameInstance() # this one is for coop

activeGames = {}

aiGames = {}