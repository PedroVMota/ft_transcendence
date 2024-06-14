from typing import Iterable
from django.db import models
from django.db.models import JSONField
from Auth.models import MyUser
import json

class ShellColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[31m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW = '\033[33m'



class GameFinalMessage:
    def Score(room, player, score, message):
        return {
            "Room": room,
            "Player": player,
            "Score": score,
            "Message": message
        }
    def Winner(room, winner, score, message):
        return {
            "Room": room,
            "Winner": winner,
            "Score": score,
            "Message": message
        }
    def Loser(room, loser, score, message):
        return {
            "Room": room,
            "Loser": loser,
            "Score": score,
            "Message": message
        }
    
class GameStatus:
    WAITING = "waiting"
    PLAYING = "playing"
    FINISHED = "finished"

class Ball: 
    def __init__(self) -> None:
        self.pos: dict = {
            "x": 0,
            "y": 0
        }
        self.lastPlayerHitRef = None
    def setLastPlayerHitRef(self, player):
        self.lastPlayerHitRef = player

    def to_dict(self):
        return {
            "Position": {
                "x": 0,
                "y": 0
            },
            "LastPlayerHit": self.lastPlayerHitRef
        }

        
    
class Paddle:
    DESLOCATIONOFFSET = 0.3
    def __init__(self, player) -> None:
        self.pos: dict = {
            "x": 0,
            "y": 0
        }
        self.playerScore: float = 0
        self.playerSpeed: float = 0
        self.playerHeight: float = 1
        self.playerWidth: float = 1
        self.playerName: str = player

    
    def to_dict(self) -> dict:
        return {
            "Position": {
                "x": self.pos["x"],
                "y": self.pos["y"]
            },
            "Score": self.playerScore,
            "Speed": self.playerSpeed,
            "Height": self.playerHeight,
            "Width": self.playerWidth,
            "Name": self.playerName
        }

    
def get_default_ball():
    ball = Ball()
    return ball.to_dict()

def get_default_paddle(player):
    paddle = Paddle(player)
    return paddle.to_dict()

# Room Model:
# This model is used to store the room data
class Room(models.Model):
    roomName = models.CharField(max_length=1000000, null=False, blank=False, default="Default")
    paddles = JSONField(null=False, blank=False, default=dict)
    paddlesCount = models.IntegerField(default=0)
    ball = JSONField(null=False, blank=False, default=get_default_ball)
    gameStatus = models.CharField(max_length=100, null=False, blank=False, default=GameStatus.WAITING)
    roomMaxPlayers = models.IntegerField(default=2)
    spectatorsMax = models.IntegerField(default=100)
    spectators = JSONField(null=False, blank=False, default=list)
    winner = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)


    def save(self, *args, **kwargs):
        print(ShellColors.OKCYAN, ("Room saved: %s" % self.roomName), ShellColors.ENDC)
        return super().save(*args, **kwargs)
    
    def addPlayer(self, playerName):
        if self.paddlesCount < self.roomMaxPlayers:
            self.paddlesCount += 1
            self.paddles[playerName] = get_default_paddle(playerName)
            print(ShellColors.OKCYAN, ("Player added to room: %s" % self.roomName), ShellColors.ENDC)
            print(ShellColors.OKCYAN, ("Players in room: %s" % self.paddles), ShellColors.ENDC)
            self.save()
            return True
        return False

    def removePlayer(self, playerName):
        if playerName in self.paddles:
            self.paddlesCount -= 1
            del self.paddles[playerName]
            print(ShellColors.RED, ("Player removed from room: %s" % self.roomName), ShellColors.ENDC)
            self.save()
            return True
        return False
    

    def addSpectator(self, spectator):
        if len(self.spectators) < self.spectatorsMax:
            self.spectators.append(spectator)
            print(ShellColors.OKCYAN, ("Spectator added to room: %s" % self.roomName), ShellColors.ENDC)
            return True
        return False
    
    def removeSpectator(self, spectator):
        if spectator in self.spectators:
            self.spectators.remove(spectator)
            return True
        return False
    
    def __str__(self):
        return self.roomName
    

    def Detail(self):

        data = {
            "Room": self.roomName,
            "Players": self.paddles,
            "PlayersCount": self.paddlesCount,
            "Ball": self.ball,
            "GameStatus": self.gameStatus
        }
        return json.dumps(data, indent=4)