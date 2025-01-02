
from threading import Lock

from math import sin, cos, atan, pi
from unicodedata import normalize


class Ball:
    def __init__(self):
        self.xPos = 100
        self.yPos = 50
        self.direction = pi # angle
        self.speed = 1
        self.lock = Lock()


    def tick(self):
        self.yPos += self.speed * sin(self.direction)
        self.xPos += self.speed * cos(self.direction)


    def normalize_direction_angle(self):
        new_direction_angle = self.direction % pi

        self.direction = new_direction_angle


    def reset_coordinates(self):
        self.xPos = 100
        self.yPos = 50


    def check_collision(self, pos):
        distance_to_paddle = pos - self.yPos
        print("distance to paddle is: ", abs(distance_to_paddle))

        if abs(distance_to_paddle) < 10:
            new_x = cos(self.direction)
            new_y = -sin(self.direction)
            new_angle = atan(new_y / new_x)
            self.direction = new_angle
            self.normalize_direction_angle()
            print("changing angle to :", self.direction)
            return True
        else:
            return False



    def get_dict(self):
        self.lock.acquire()
        to_return = dict(x=self.xPos, y=self.yPos)
        self.lock.release()

        return to_return