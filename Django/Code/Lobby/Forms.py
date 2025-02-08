
from django import forms
from .models import Lobby

# class Lobby(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True) # Unique ID for the game
    # name = models.CharField(max_length=255, null=True, blank=True) # Name of the room
    # players = models.ManyToManyField(MyUser, related_name='players', blank=True) # Player One
    # game = models.ForeignKey(Game, related_name='game', on_delete=models.CASCADE, null=True, blank=True) # Player Two
    # def __str__(self):
        # return f"{self.name}"
    
"""
FORM TO CREATE THE LOBBY IS ONLY REQUIRED NAME OF THE LOBBY
there is a method that getter of the lobby class.
"""
class LobbyForm(forms.ModelForm):
    class Meta:
        model = Lobby
        # todo -> change this to somewhere in the Lobby module
        fields = ['name']