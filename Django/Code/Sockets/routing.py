# Sockets/routing.py
from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path('ws/game/<str:room_name>/', consumers.PongGameConsumer.as_asgi()),
    re_path('ws/notifications/', consumers.NotificationsConsumer.as_asgi()),
    re_path(r'ws/privchat/(?P<uuid>[^/]+)/$', consumers.PrivateChatConsumer.as_asgi()),
]


