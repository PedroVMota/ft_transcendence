
from Lobby.models import Lobby as LobbyModel

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import json

# re_path(r'ws/Lobby/(?P<lobby_id>[\w-]+)/$', consumers.LobbyConsumer.as_asgi()),
# class MonitorLobbyConsumer(AsyncWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#         self.room_group_name = None
#
#     async def connect(self):
#         if self.scope["user"].is_anonymous:
#             await self.close()
#             if not self.scope["user"].is_superuser:
#                 await self.close()
#         else:
#             self.room_group_name = self.scope['url_route']['kwargs']['lobby_id']
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )
#             await self.accept()
#
#             lobby_users = await sync_to_async(lambda: list(LobbyModel.objects.filter(players=self.scope['user'])))()
#             if lobby_users:
#                 print("User already in the lobby")
#                 return
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     "type": "notification",
#                     "message": f"Player {self.scope['user'].first_name} has joined the lobby",
#                     "data": {
#                         "userCode": self.scope['user'].userSocialCode,
#                         "first_name": self.scope['user'].first_name,
#                         "last_name": self.scope['user'].last_name,
#                         "profile_picture": self.scope['user'].profile_picture.url,
#                     }
#                 }
#             )
#
#     async def notification(self, event: dict):
#         message = event['message']
#         data = event['data']
#         await self.send(text_data=json.dumps({
#             'type': 'notification',
#             'message': message,
#             'data': data
#         }))
#
#     async def disconnect(self, close_code: int):
#         # Fetch the existing data from Redis
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 "type": "notification",
#                 "message": f"Player {self.scope['user'].first_name} has left the lobby",
#                 "data": {}
#             }
#         )
#
#     async def receive(self, text_data=None, bytes_data=None):
#         print("receive")
#         print(text_data)
#         data= json.loads(text_data)
#         user = await sync_to_async(self.scope["user"].getDict)()
#         if data["action"] == "message-sent-on-lobby":
#             self.handle_lobby_message(data, user['Info'])
#
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 "type": "websocket.message",
#                 "message": data
#             }
#         )
#
#     async def websocket_message(self, event):
#         # This is called when a message is received from the group
#         await self.send(text_data=json.dumps(event["message"]))
#
#
#     @staticmethod
#     def handle_lobby_message(data, user):
#         data["action"] = "lobby-message-submission"
#         data["user"] = user['first_name']

# class LobbyConsumer(AsyncWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#         self.room_group_name = None
#         self.user = None
#
#     async def connect(self):
#         self.room_group_name = self.scope['url_route']['kwargs']['lobby_id']
#         self.user = self.scope['user']
#
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#         # Send welcome message
#         welcome_msg = {
#             'type': 'notification',
#             'message': f"You have joined the lobby {self.room_group_name}"
#         }
#         await self.send(text_data=json.dumps(welcome_msg))
#
#         # Print and log the welcome message
#         print(welcome_msg['message'])
#
#     async def disconnect(self, close_code):
#         # Remove the user from the group
#         goodbye_msg = {
#             'type': 'notification',
#             'message': f"{self.user.username} has left the lobby"
#         }
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             goodbye_msg
#         )
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     async def receive(self, text_data=None, bytes_data=None):
#         data = json.loads(text_data)
#         data['type'] = 'message'
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             data
#         )
#
#     async def notification(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'type': 'notification',
#             'message': message
#         }))
#
#     async def message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'type': 'message',
#             'message': message
#         }))