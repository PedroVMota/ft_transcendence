
from django.urls import re_path

from .module_consumers.lobbychatconsumer import LobbyChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/Monitor/Lobby/(?P<lobby_id>[\w-]+)/$', LobbyChatConsumer.as_asgi()),
]
