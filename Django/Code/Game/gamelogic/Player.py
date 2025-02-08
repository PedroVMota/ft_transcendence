
from threading import Lock

from Game.Window import Window
from Game.Camera import Camera

class Player:
    speed: int

    def __init__(self):
        self.yPos = 50
        self.score = 0
        self.name = 'default'
        self.window = Window()
        self.camera = Camera()
        self.lock = Lock()
        self.speed = 5

    def handle_paddle_movement(self, direction):
        if direction < 0 and self.yPos >= 1:
            print("moving player down")

            self.lock.acquire()
            self.yPos -= self.speed
            self.lock.release()

        elif direction > 0 and self.yPos <= 99:
            print("moving player up")

            self.lock.acquire()
            self.yPos += self.speed
            self.lock.release()

    def get_pos(self):
        return self.yPos

    def get_dict(self):
        self.lock.acquire()
        to_return = dict(y=self.yPos, score=self.score)
        self.lock.release()

        return to_return
