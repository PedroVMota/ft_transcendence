
class Camera:
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
        self.zPos = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.movementSpeed = 0.2
        self.rotationSpeed = 0.5

    def get_dict(self):
        to_return = dict(position = {'x': self.xPos, 'y': self.yPos, 'z': self.zPos},
                         rotation = {'x': self.xRot, 'y': self.yRot, 'z': self.zRot},
                         speed = self.movementSpeed)

        return to_return


    def handle_key(self, key):
        if key == "q":
            self.xPos = 0
            self.yPos = 0
            self.zPos = 10
        elif key == "n":
            self.xPos -= self.movementSpeed
        elif key == "m":
            self.xPos += self.movementSpeed
        elif key == "j":
            self.yPos -= self.movementSpeed
        elif key == "k":
            self.yPos += self.movementSpeed
        elif key == "z":
            self.zPos -= self.movementSpeed