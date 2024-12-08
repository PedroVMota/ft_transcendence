
class Ball:
    def __init__(self):
        self.xPos = 0;
        self.yPos = 0;
        self.direction = 0;
        self.speed = 0;


    def get_dict(self):
        dict = {}
        dict['x'] = self.xPos
        dict['y'] = self.yPos
        dict['direction'] = self.direction
        dict['speed'] = self.speed