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

    def getDict(self):
        return {
            "uuid": str(self.id),
            "RoomName": self.roomName,
            "PlayerOne":  self.pOne.id if self.pOne is not None else None,
            
            "PlayerTwo": self.pTwo.id if self.pTwo is not None else None,
            "Winner": self.winner.uuid if self.winner is not None else None,
            "State": self.state,
            "WebSocketId": str(self.webSocketId),
            "WebSocketChatID": str(self.webSocketChatID),
            "TypeGame": self.gameType,
        }


class Lobby(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True) # Unique ID for the game
    name = models.CharField(max_length=255, null=True, blank=True) # Name of the room
    players = models.ManyToManyField(MyUser, related_name='players', ) # Player One
    game = models.ForeignKey(Game, related_name='game', on_delete=models.CASCADE, null=True, blank=True) # Player Two

    def save(self, *args, **kwargs):
        # Create a new game if one does not already exist
        print("SAVING LOBBY MODULE")
        if self.game is None:
            self.game = Game.objects.create()  # Adjust initialization with any required fields for Game
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    def joinPlayer(self, user: MyUser):
        if user in self.players:
            raise Exception("Already in the game")
        if self.players < 2:
            self.players.add(user)
            self.game.join(user)
        self.save()


    
    def getPlayerData(self):
        return [player.getDict() for player in self.players.all()]
    
    def isAvailable(self):
        return self.players.count() < 2 # If there are less than 2 players, the lobby is available

    def getDict(self):
        return {
            "uuid": str(self.id),
            "Name": self.name,
            "Players": self.getPlayerData(),
            "Game": self.game.getDict() if self.game is not None else None,
        }
    

    