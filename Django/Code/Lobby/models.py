
from Auth.models import MyUser
from django.db import models
from Game.models import Game as GameMode
import uuid

class Lobby(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)  # Unique ID for the game
    name = models.CharField(max_length=255, null=True, blank=True)  # Name of the room
    players = models.ManyToManyField(MyUser, related_name='players', )  # Player One
    game = models.ForeignKey(GameMode, related_name='game', on_delete=models.CASCADE, null=True, blank=True)  # Player Two

    def save(self, *args, **kwargs):
        # Create a new game if one does not already exist
        print("SAVING LOBBY MODULE")
        if self.game is None:
            self.game = GameMode.objects.create()  # Adjust initialization with any required fields for Game
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    def joinPlayer(self, user: MyUser):
        if self.players.filter(id=user.id).exists():
            raise Exception("Already in the game")
        else:
            if len(self.players.all()) < 2:
                self.players.add(user)
                self.game.joinPlayer(user)
                print("added player to lobby")
        self.save()

    def isFull(self):
        return self.players.count() == 2

    def disconnectPlayer(self, user: MyUser):
        print("========= DISCONNECT PLAYER =========")
        if self.players.filter(id=user.id).exists():
            print(f"[DISCONNECT PLAYER] User {user.id} exists in the lobby")
            self.players.remove(user)
            print(f"[DISCONNECT PLAYER] User {user.id} removed from the lobby")
            self.game.removePlayer(user)
            print(f"[DISCONNECT PLAYER] User {user.id} removed from the game")
            if self.game.pOne is None and self.game.pTwo is None:
                print("[DISCONNECT PLAYER] Both players are None, deleting the game")
                self.game.delete()
            if self.players.count() == 0:
                print("No players left in the lobby, deleting the lobby")
                self.delete()
                return
            self.save()
        else:
            pass

    def getPlayerData(self):
        return [player.getDict() for player in self.players.all()]

    def isAvailable(self):
        return self.players.count() < 2  # If there are less than 2 players, the lobby is available

    def getDict(self):
        return {
            "uuid": str(self.id),
            "Name": self.name,
            "Players": self.getPlayerData(),
            "Game": self.game.getDict() if self.game is not None else None,
        }