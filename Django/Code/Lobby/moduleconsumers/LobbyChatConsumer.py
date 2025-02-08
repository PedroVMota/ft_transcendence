
from Lobby.models import Lobby as LobbyModel

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import json

class LobbyChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None


    async def is_user_already_in_lobby(self) -> bool:
        lobby_users = await sync_to_async(lambda: LobbyModel.objects.filter(players=self.scope['user']))()
        return lobby_users is not None


    async def send_connection_was_successful(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "notification",
                "message": f"Player {self.scope['user'].first_name} has joined the lobby",
                "data": {
                    "userCode": self.scope['user'].userSocialCode,
                    "first_name": self.scope['user'].first_name,
                    "last_name": self.scope['user'].last_name,
                    "profile_picture": self.scope['user'].profile_picture.url,
                }
            }
        )

    async def send_message_with_data(self, event: dict):
        message = event['message']
        data = event['data']
        type_name = event['type_name']
        await self.send(text_data=json.dumps({
            'type': type_name,
            'message': message,
            'data': data
        }))


    async def send_message(self, event: dict):
        await self.send(text_data=json.dumps(
            event['message']
        ))


    @staticmethod
    def handle_lobby_message(data: dict, user_info):
        data["action"] = "lobby-message-submission"
        data["user"] = user_info["first_name"]


    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            self.room_group_name = self.scope['url_route']['kwargs']['lobby_id']
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            user_already_in_lobby = await self.is_user_already_in_lobby()
            if not user_already_in_lobby:
                await self.send_connection_was_successful()
            else:
                print("User already in lobby")
                return


    async def disconnect(self, close_code: int):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send.message.with.data",
                "message": f"Player {self.scope['user'].first_name} has left the lobby",
                "data": {}
            }
        )


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        user = await sync_to_async(self.scope["user"].getDict)()

        if data["action"] == "message-sent-on-lobby":
            self.handle_lobby_message(data, user['Info'])

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send.message",
                "message": data
            }
        )


