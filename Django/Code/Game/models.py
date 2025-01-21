from email.policy import default
from typing import Iterable
from Auth.models import MyUser
from django.db import models
from Chat.models import currentChat
import uuid


GameStates = (
    (0, 'Waiting'),
    (1, 'In Progress'),
    (2, 'Completed'),
    (3, 'Cancelled'),
)

GameType = (
    # ("Matchmaking", "Matchmaking"),
    ("Friendly", "Friendly"),
)


class Game(models.Model):

    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True) # Unique ID for the game
    roomName = models.CharField(max_length=255, null=True, blank=True) # Name of the room
    pOne = models.ForeignKey(MyUser, related_name='First_Player', on_delete=models.CASCADE, null=True, blank=True) # Player One
    pTwo = models.ForeignKey(MyUser, related_name='Second_Player', on_delete=models.CASCADE, null=True, blank=True) # Player Two
    winner = models.ForeignKey(MyUser, related_name='won_games', on_delete=models.SET_NULL, null=True, blank=True) # Winner of the game
    state = models.IntegerField(choices=GameStates, default=0)  # State of the game
    webSocketId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # Unique ID for the WebSocket
    webSocketChatID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # Unique ID for the WebSocket Chat
    gameType = models.CharField(choices=GameType, default="Friendly", max_length=20) # Type of the game


    def __str__(self):
        return f"{self.id}"
    
    def joinPlayer(self, user: MyUser):
        if user in [self.pOne, self.pTwo]:
            raise Exception("Already in the game")
        if self.pOne is None:
            self.pOne = user
        elif self.pTwo is None:
            self.pTwo = user
        else:
            raise Exception("Game is full")
        self.save()

    def removePlayer(self, user: MyUser):
        if user in [self.pOne, self.pTwo]:
            if user == self.pOne:
                self.pOne = None
            elif user == self.pTwo:
                self.pTwo = None
        else:
            raise Exception("User is not in the game")
        self.save()

    def getDict(self):
        return {
            "uuid": str(self.id),
            "RoomName": self.roomName,
            "PlayerOne":  self.pOne.getDict() if self.pOne is not None else None,
            
            "PlayerTwo": self.pTwo.getDict() if self.pTwo is not None else None,
            "Winner": self.winner.uuid if self.winner is not None else None,
            "State": self.state,
            "WebSocketId": str(self.webSocketId),
            "WebSocketChatID": str(self.webSocketChatID),
            "TypeGame": self.gameType,
        }
    

class GameHistory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    game_id = models.CharField(default="")
    playerOne = models.CharField(default="")
    playerTwo = models.CharField(default="")
    winner = models.CharField(default="")
    playerOneScore = models.IntegerField(default=0)
    playerTwoScore = models.IntegerField(default=0)
    