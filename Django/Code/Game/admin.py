from django.contrib import admin
from .models import Lobby, Game, GameHistory

# Register your models here
admin.site.register(Lobby)
admin.site.register(Game)
admin.site.register(GameHistory)
