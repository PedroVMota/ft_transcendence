# Sockets/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async




    
class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomName = self.scope['url_route']['kwargs']['room_name']
        self.roomGroup = "pong_%s" % self.roomName
        # Use sync_to_async to perform the synchronous database query
        try:
            self.room = await sync_to_async(Room.objects.get)(roomName=self.roomName)
        except Room.DoesNotExist:
            # If the room doesn't exist, create a new one
            self.room = await sync_to_async(Room.objects.create)(roomName=self.roomName)
# 
        await sync_to_async(self.room.addPlayer)(self.scope["user"].username)

        self.room_group_name = 'pong_%s' % self.roomName
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(ShellColors.BOLD, ("Connected to room: %s" % self.roomName), ShellColors.ENDC)
        await sync_to_async(self.room.save)()

        self.channel_layer.group_send(
            self.room_group_name,
            {
                'Type': 'Join',
                'message': 'Player joined the room'
            }
        )



    async def disconnect(self, close_code):
        print(ShellColors.RED, ("Player removed from room: %s" % self.roomName), ShellColors.ENDC)
        await sync_to_async(self.room.removePlayer)(self.scope["user"].username)
        if(len(self.room.players) == 0):
            print(ShellColors.RED, ("Room deleted: %s" % self.roomName), ShellColors.ENDC)
            await sync_to_async(self.room.delete)()
        else:
            await sync_to_async(self.room.save)()  # Save the room after removing the player
        await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
    )

    async def receive(self, text_data=None, bytes_data=None):
        print(ShellColors.YELLOW, ("Received data: %s" % text_data), ShellColors.ENDC)
        self.room = await sync_to_async(Room.objects.get)(roomName=self.roomName)
        print(self.room.Detail())
        # text_data_json = json.loads(text_data)
        # Type = text_data_json['Type']
        # message = text_data_json['message']

        # if Type == "Join":
            # await self.channel_layer.group_send(
                # self.room_group_name,
                # {
                    # 'Type': 'Join',
                    # 'message': message
                # }
            # )





# path('ws/general/', consumers.GeneralConsumer.as_asgi()),
"""
This websocket is used for general web funcionalities like:
- Notifications
- Friend requests


It's completly separated from the game.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GeneralConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroup = "chat_Room_with_%s" % self.scope["user"].username
        await self.channel_layer.group_add(
            self.roomGroup,
            self.channel_name
        )
        await self.accept()
        print("WebSocket connection accepted")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroup,
            self.channel_name
        )
        print("WebSocket connection closed")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Received data: %s" % data)
        message_type = data.get('type')

        if message_type == 'ping':
            # Handle ping message
            await self.send(text_data=json.dumps({'type': 'pong'}))
            return

        message = data.get('message')
        username = self.scope["user"].username

        if message and username:
            print("UserData: %s" % username + ": " + message)
            await self.channel_layer.group_send(
                self.roomGroup,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        print("WebSocket connection accepted")
        print(f"User: {user.username} and Code: {user.userSocialCode}")
        if user.is_anonymous:
            await self.close()
        else:
            # Group the user by their userSocialCode
            self.group_name = f"user_{user.userSocialCode}"
            print("Group Name: ", self.group_name)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
    async def disconnect(self, close_code):
        # Remove the user from the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    async def send_notification(self, event):
        # Send notification data to the WebSocket
        await self.send(text_data=json.dumps({
            'notifications': event['notifications']
        }))
