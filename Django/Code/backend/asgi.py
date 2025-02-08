# asgi.py

from Game import routing as GameWebSocketRoutes
from Lobby import routing as LobbyWebSocketRoutes
from Notification import routing as NotificationRoutes
from Chat import routing as ChatRoutes

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            GameWebSocketRoutes.websocket_urlpatterns
                + NotificationRoutes.websocket_urlpatterns
                + ChatRoutes.websocket_urlpatterns
                + LobbyWebSocketRoutes.websocket_urlpatterns
        )
    ),
})
