
from threading import Lock

from math import sin, cos, dist, pi
from unicodedata import normalize


class Ball:
    def __init__(self):
        self.xPos = 100
        self.yPos = 50
        self.direction = pi # angle
        self.speed = 0
        self.lock = Lock()


    def tick(self):
        self.yPos += self.speed * sin(self.direction)
        self.xPos += self.speed * cos(self.direction)



    def normalize_direction_angle(self):
        new_direction_angle = self.direction % (pi * 2)

        self.direction = new_direction_angle


    def reset_coordinates(self):
        self.xPos = 100
        self.yPos = 50


    def check_collision(self, pos):
        distance_to_paddle = dist(pos, self.yPos)

        if abs(distance_to_paddle) < 10:
            old_direction_abs = 2 * pi - self.direction
            self.normalize_direction_angle()
            self.direction = 2 * pi - (old_direction_abs * (10 - distance_to_paddle) / 10)
            self.normalize_direction_angle() # todo: check this logic
            return True
        else:
            return False



    def get_dict(self):
        self.lock.acquire()
        to_return = dict(x=self.xPos, y=self.yPos)
        self.lock.release()

        return to_return