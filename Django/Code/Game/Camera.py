
class Camera:
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
        self.zPos = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

    def get_dict(self):
        to_return = dict(position = {'x': self.xPos, 'y': self.yPos, 'z': self.zPos},
                         rotation = {'x': self.xRot, 'y': self.yRot, 'z': self.zRot})

        return to_return

    def handle_key(self, key):
        if (key == 'q')