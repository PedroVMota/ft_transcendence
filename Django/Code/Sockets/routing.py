# Sockets/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # path('ws/', consumers.YourConsumer.as_asgi()),
    path('ws/Game/<str:room_name>/', consumers.GameConsumer.as_asgi()),
]


