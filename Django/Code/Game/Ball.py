
from threading import Lock

from math import sin, cos, atan2, pi
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

    def reflection_on_axis(self, x_axis):
        if x_axis:
            self.direction = -self.direction
        else:
            reflected_angle = pi - self.direction

            self.direction = atan2(sin(reflected_angle), cos(reflected_angle))

    def normalize_direction_angle(self, pipi):
        self.direction = atan2(sin(self.direction), cos(self.direction))
        print("changing angle to :", self.direction)


    def reset_coordinates_and_speed(self):
        self.xPos = 100
        self.yPos = 50
        self.speed = 1


    def check_collisions_y_axis(self):
        if self.yPos <= 0 or self.yPos >= 100:
            # new_x = -cos(self.direction)
            # new_y = sin(self.direction)
            # new_angle = atan(new_y / new_x)
            # self.direction = new_angle
            self.reflection_on_axis(True)
            self.normalize_direction_angle(pi)
            self.tick()
            self.speed += 0.05

    def check_collision_x_axis(self, pos):
        distance_to_paddle = pos - self.yPos
        print("distance to paddle is: ", abs(distance_to_paddle))

        if abs(distance_to_paddle) < 12:
            offset = distance_to_paddle / 12
            # new_x = cos(self.direction)
            # new_y = -sin(self.direction)
            # new_angle = atan(new_y / new_x)
            self.reflection_on_axis(False)
            self.direction += 0.5 * offset
            self.normalize_direction_angle(pi)
            self.tick()
            self.speed += 0.05
            return True
        else:
            return False



    def get_dict(self):
        self.lock.acquire()
        to_return = dict(x=self.xPos, y=self.yPos)
        self.lock.release()

        return to_return