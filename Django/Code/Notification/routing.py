# Sockets/routing.py
from django.urls import re_path
# import Consumers.NotificationMenu
from .Consumers.NotificationMenu import NotificationsConsumer
from .Consumers.Lobby import LobbyConsumer
websocket_urlpatterns = [
    re_path(r'ws/notifications/', NotificationsConsumer.as_asgi()),
    re_path(r'ws/connect/lobby/(?P<lobby_id>[0-9a-f-]{36})/', LobbyConsumer.as_asgi()),
    
]


