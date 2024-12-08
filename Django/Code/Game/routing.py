# Sockets/routing.py
from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/game/(?P<room_name>[^/]+)/$', consumers.PongGameConsumer.as_asgi()),
    re_path(r'ws/Monitor/Game/', consumers.MonitorGameConsumer.as_asgi()),
]
