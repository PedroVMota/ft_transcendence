# Sockets/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from .models import Room
from .models import ShellColors



    
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
