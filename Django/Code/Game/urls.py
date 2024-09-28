from django.urls import path, include
from . import views


"""
MODELS:


class Game(models.Model):
    pOne = models.ForeignKey(MyUser, related_name='games', on_delete=models.CASCADE) # Player One
    pTwo = models.ForeignKey(MyUser, related_name='games', on_delete=models.CASCADE) # Player Two

    winner = models.ForeignKey(MyUser, related_name='won_games', on_delete=models.SET_NULL, null=True, blank=True) # Winner of the game


    state = models.IntegerField(choices=GameStates, default=2) # State of the game


    webSocketId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # Unique ID for the WebSocket
    webSocketChatID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # Unique ID for the WebSocket Chat


    gameType = models.CharField(choices=GameType, default="Friendly", max_length=20) # Type of the game


    def __str__(self):
        return f"{self.uuid}"
    
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
            "uuid": str(self.uuid),
            "PlayerOne": self.pOne.uuid,
            "PlayerTwo": self.pTwo.uuid,
            "Winner": self.winner.uuid if self.winner is not None else None,
            "State": self.state,
            "WebSocketId": self.webSocketId,
            "WebSocketChatID": self.webSocketChatID,
            "TypeGame": self.gameType,
        }



class Tournament(models.Model):
    uniqueId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # Game Players
    players = models.ManyToManyField(MyUser, related_name='tournaments') # Players in the tournament
    maxPlayers = models.IntegerField(default=8) # Max players in the tournament
    winner = models.ForeignKey(MyUser, related_name='won_tournaments', on_delete=models.SET_NULL, null=True, blank=True) # Winner of the tournament

    # Comunication System
    WebSocketId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # Unique ID for the WebSocket
    WebSocketOfChat = models.ForeignKey(currentChat, related_name='tournament_chat', on_delete=models.CASCADE, null=True, blank=True)

    # Game Info
    award = models.DecimalField(max_digits=10, decimal_places=2) # Award for the winner
    JoinCost = models.DecimalField(max_digits=10, decimal_places=2) # Cost to join the tournament

    allMatches = models.ManyToManyField(Game, related_name='tournaments_matches') # Pre setup the matches for all the players, and then start the tournament


    GameHistory = models.ManyToManyField(Game, related_name='tournaments')


    def getDict(self):
        return {
            "uuid": str(self.uuid),
            "players": [player.getDict() for player in self.players.all()],
            "maxPlayers": self.maxPlayers,
            "winner": self.winner.uuid if self.winner is not None else None,
            "WebSocketId": self.WebSocketId,
            "WebSocketOfChat": self.WebSocketOfChat.uuid if self.WebSocketOfChat is not None else None,
            "award": self.award,
            "JoinCost": self.JoinCost,
            "allMatches": [match.uuid for match in self.allMatches.all()],
            "GameHistory": [game.uuid for game in self.GameHistory.all()],
        }


    def __str__(self):
        return f"{self.uuid}"
    
    def join(self, user: MyUser):
        if 0 > user.wallet.balance - self.JoinCost:
            raise Exception("Not enough balance")
        if self.players.filter(uuid=user.uuid).exists():
            raise Exception("Already in the tournament")
        user.Wallet.makeTransaction(self.JoinCost, 'Transfer', f"{self.uuid} Join Cost")
        self.players.add(user)
        self.award += self.JoinCost
        self.save()

    def leave(self, user: MyUser):
        if not self.players.filter(uuid=user.uuid).exists():
            raise Exception("Not in the tournament")
        self.players.remove(user)

    def eliminate(self, uuidOfUser: str):
        user = MyUser.objects.get(uuid=uuidOfUser)
        if not self.players.filter(uuid=user.uuid).exists():
            raise Exception("Not in the tournament")
        self.players.remove(user)
"""

#example: /Game/
urlpatterns = [
    path('Create/', views.CreateIndividualGame), # Create a game

    path('Monitor/', views.locaIndex, name='locaIndex'), # Index of the game
] 
