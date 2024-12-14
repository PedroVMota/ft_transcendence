
from Game.Window import Window
from Game.Camera import Camera

class Player:
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
        self.score = 0
        self.window = Window()
        self.camera = Camera()

    def handle_movement_key(self, key):
        if key == 'w':
            print("moving player up")
            self.xPos -= 1
        if key == 's':
            print("moving player down")
            self.xPos += 1

    def handle_camera_key(self, key):


    def get_dict(self):
        to_return = dict(x=self.xPos, y=self.yPos, score=self.score)

        return to_return
