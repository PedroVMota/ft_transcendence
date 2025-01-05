# Sockets/routing.py
from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/game/(?P<room_name>[^/]+)/$', consumers.PongGameConsumer.as_asgi()),
    re_path(r'ws/Monitor/Game/', consumers.MonitorGameConsumer.as_asgi()),



    re_path(r'ws/Monitor/Lobby/(?P<lobby_id>[\w-]+)/$', consumers.MonitorLobbyConsumer.as_asgi()),
    re_path(r'ws/Game/(?P<game_id>[\w-]+)$', consumers.MultiplayerGame.as_asgi())


]