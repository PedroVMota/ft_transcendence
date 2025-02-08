from platform import release

from Game.gamelogic.GameObject import GameObject

from math import ceil, cos, tan, fabs
from time import sleep

import threading

class AILoop(threading.Thread):
    def __init__(self, game_ref: GameObject):
        super().__init__()
        # a reference to already initialized game object
        self.gameObject: GameObject = game_ref


    @staticmethod
    def transform_offset_in_actual_position(y_offset: int) -> int:
        predicted_position: int = 0
        while y_offset > 100 or y_offset < 0:
            if y_offset > 100:
                predicted_position = 100 - (y_offset - 100)
            elif y_offset < 0:
                predicted_position = int(fabs(y_offset))

        return predicted_position


    def predict_ball_position(self):
        predicted_offset = (200 - self.gameObject.ball.xPos * tan(self.gameObject.ball.direction)) + 50

        return self.transform_offset_in_actual_position(predicted_offset)


    def acquire_locks(self):
        self.gameObject.playerOne.lock.acquire()
        self.gameObject.playerTwo.lock.acquire()
        self.gameObject.ball.lock.acquire()


    def release_locks(self):
        self.gameObject.playerOne.lock.release()
        self.gameObject.playerTwo.lock.release()
        self.gameObject.ball.lock.release()


    def nonblocking_yield_loop(self, seconds: float):
        self.release_locks()
        sleep(seconds)
        self.acquire_locks()


    def nonblocking_move_paddle(self, direction: int):
        self.release_locks()
        self.gameObject.playerTwo.handle_paddle_movement(direction)
        self.acquire_locks()


    def react_to_prediction(self, predicted_position: int) -> None:
        self.acquire_locks()
        offset_to_predicted_position = self.gameObject.playerOne.yPos - predicted_position
        number_of_steps = ceil(fabs(offset_to_predicted_position) / self.gameObject.playerTwo.speed)
        original_n_of_steps = number_of_steps # just to store the value for later

        if number_of_steps <= 0:
            self.nonblocking_yield_loop(1.0)
        else:
            while number_of_steps > 0:
                if offset_to_predicted_position < -5:
                    self.nonblocking_move_paddle(1)
                elif offset_to_predicted_position > 5:
                    self.nonblocking_move_paddle(-1)
                number_of_steps -= 1
                self.nonblocking_yield_loop(1 / original_n_of_steps)

        self.release_locks()


    def run(self):
        while True:
            if self.gameObject.running and self.gameObject.playing:
                # check if the ball is going in direction of the right wall
                if cos(self.gameObject.ball.direction) > 0:
                    predicted_position = self.predict_ball_position()
                    self.react_to_prediction(predicted_position)

