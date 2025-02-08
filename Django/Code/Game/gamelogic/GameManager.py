
from Game.Game import GameLoop, AILoop


class GameManager:
    def __init__(self, aiIncluded=False):
        self.gameLoop: GameLoop = GameLoop()
        self.aiLoop = None

        if aiIncluded:
            self.aiLoop = AILoop(self.gameLoop.game)

        self.gameLoop.start()
        if self.aiLoop is not None:
            self.aiLoop.start()
        