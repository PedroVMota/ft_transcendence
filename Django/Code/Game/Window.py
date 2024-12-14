
class Window:
    def __init__(self):
        self.width = 0
        self.height = 0

    def get_dict(self):
        to_return = dict(width = self.width, height = self.height)

        return to_return