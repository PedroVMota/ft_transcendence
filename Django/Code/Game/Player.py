

class Player:
    def __init__(self):
        self.xPos = 0;
        self.yPos = 0;
        self.score = 0;

    def handle_key(self, key):
        if key == 'w':
            print("moving player up")
            self.xPos -= 1
        if key == 's':
            print("moving player down")
            self.xPos += 1

    def get_dict(self):
        dict = {}
        dict['x'] = self.xPos
        dict['y'] = self.yPos
        dict['score'] = self.score

        return dict
