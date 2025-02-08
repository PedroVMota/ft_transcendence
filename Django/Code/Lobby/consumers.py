from django.conf import LazySettings

from Lobby.models import Lobby as LobbyModel

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import json
import redis



settings = LazySettings()

# todo -> do we need this???
redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)

# re_path(r'ws/Lobby/(?P<lobby_id>[\w-]+)/$', consumers.LobbyConsumer.as_asgi()),
class MonitorLobbyConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None

    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
            if not self.scope["user"].is_superuser:
                await self.close()
        else:
            self.room_group_name = self.scope['url_route']['kwargs']['lobby_id']
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            lobby_users = await sync_to_async(lambda: list(LobbyModel.objects.filter(players=self.scope['user'])))()
            if lobby_users:
                print("User already in the lobby")
                return
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

    async def notification(self, event: dict):
        message = event['message']
        data = event['data']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message,
            'data': data
        }))

    async def disconnect(self, close_code: int):
        # Redis key for the lobby
        redis_key = f"lobby:{self.scope['url_route']['kwargs']['lobby_id']}"
        # Fetch the existing data from Redis
        existing_data = await sync_to_async(redis_instance.get)(redis_key)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "notification",
                "message": f"Player {self.scope['user'].first_name} has left the lobby",
                "data": {}
            }
        )

        if existing_data:
            # Decode and load the existing data
            decoded_result = existing_data.decode("utf-8")
            lobby_data = json.loads(decoded_result)

            # Decrement the SizeOfPlayers if greater than 0
            if lobby_data["data"]["SizeOfPlayers"] > 0:
                lobby_data["data"]["SizeOfPlayers"] -= 1

            # Save the updated data back to Redis
            updated_data = json.dumps(lobby_data)
            await sync_to_async(redis_instance.set)(redis_key, updated_data)



            print(f"Updated Lobby Data after disconnection: {updated_data}")
        else:
            print(f"Lobby data not found for key: {redis_key}")



    async def receive(self, text_data=None, bytes_data=None):
        print("receive")
        print(text_data)
        data= json.loads(text_data)
        user = await sync_to_async(self.scope["user"].getDict)()
        #print("consumer.receive printing its scope: ", user)
        # todo ? await sync_to_async(redis_instance.set)(redis_key, serialized_data)
        if data["action"] == "message-sent-on-lobby":
            self.handle_lobby_message(data, user['Info'])

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "websocket.message",
                "message": data
            }
        )

    async def websocket_message(self, event):
        # This is called when a message is received from the group
        await self.send(text_data=json.dumps(event["message"]))


    @staticmethod
    def handle_lobby_message(data, user):
        data["action"] = "lobby-message-submission"
        data["user"] = user['first_name']