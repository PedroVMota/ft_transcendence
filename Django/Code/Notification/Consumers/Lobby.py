
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from Lobby.models import Lobby

import json
# re_path(r'ws/connect/lobby/(?P<lobby_id>[0-9a-f-]{36})/', LobbyConsumer.as_asgi()),


class LobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.lobby_id = self.scope['url_route']['kwargs']['lobby_id']
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
        self.room_group_name = f'lobby_{self.lobby_id}'
        await self.accept()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def refresh(self, event):
        await self.send(text_data=json.dumps({
            'action': 'refresh',
        }))

    async def disconnect(self):
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type': 'refresh',
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()