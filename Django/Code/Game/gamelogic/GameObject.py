
from .Ball import Ball
from .Player import Player

from math import cos

class GameObject:
    def __init__(self):
        self.playerOne = Player()
        self.playerTwo = Player()
        self.ball = Ball()
        self.playing: bool = False
        self.running: bool = True


    def __del__(self):
        self.playing = False

    def collision_detected(self) -> bool:
        return self.ball.xPos <= 2 or self.ball.xPos >= 198

    def goal_detected(self) -> bool:
        return (not self.ball.check_collision_x_axis(self.playerOne.yPos)
                or not self.ball.check_collision_x_axis(self.playerTwo.yPos))

    def tick(self):
        self.ball.tick()
        # check if the ball is going in direction of the left wall
        if cos(self.ball.direction):
            if self.collision_detected() and self.goal_detected():
                self.playerTwo.score += 1
                self.ball.reset_coordinates_and_speed()
        else: # if not the ball is in direction of the right wall
            if self.collision_detected() and self.goal_detected():
                self.playerOne.score += 1
                self.ball.reset_coordinates_and_speed()