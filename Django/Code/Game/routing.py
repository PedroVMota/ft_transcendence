# Sockets/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/Monitor/Game/', consumers.MonitorGameConsumer.as_asgi()),
    re_path(r'ws/Game/(?P<game_id>[\w-]+)$', consumers.MultiplayerGame.as_asgi())
]
