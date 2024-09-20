# Sockets/routing.py
from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path('ws/notifications/', consumers.NotificationsConsumer.as_asgi()),
]


