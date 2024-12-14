
class Ball:
    def __init__(self):
        self.xPos = 0;
        self.yPos = 0;
        self.direction = 0;
        self.speed = 0;


    def get_dict(self):
        to_return = dict(x=self.xPos, y=self.yPos, direction=self.direction, speed=self.speed)

        return to_return