# Sockets/routing.py
from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/privchat/(?P<uuid>[^/]+)/$', consumers.PrivateChatConsumer.as_asgi()),
]


