# Sockets/routing.py
from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    # re_path('ws/Game/<str:room_name>/', consumers.GameConsumer.as_asgi()),
    # re_path('ws/general/', consumers.GeneralConsumer.as_asgi()),
    re_path('ws/notifications/', consumers.NotificationsConsumer.as_asgi()),
    re_path(r'ws/privchat/(?P<uuid>[^/]+)/$', consumers.PrivateChatConsumer.as_asgi()),
]


