# Sockets/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class GeneralChat(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'general'
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user.username} has joined the chat.'
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        
        await self.channel_layer.send({
            'type': 'chat_message',
            'message': f'{self.user.username} has left the chat.'
        })

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': self.user.username + ': ' + message
        }))