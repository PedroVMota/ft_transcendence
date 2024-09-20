# Sockets/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json
from Auth.models import Conversation, currentChat
from channels.db import database_sync_to_async
from django.utils import timezone

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['uuid']
        self.room_group_name = f'privchat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Fetch previous messages
        previous_messages = await self.get_previous_messages(self.room_name)

        # Send previous messages to the client
        for message in previous_messages:
            await self.send(text_data=json.dumps({
                'message': message['Message'],
                'user': message['AuthorOfTheMessage__username'],
                'create_date': message['create_date'].strftime('%Y-%m-%d %H:%M:%S')
            }))

        # Join the room group

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Save the new message to the database
        await self.save_message(self.user, self.room_name, message)

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'create_date': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send the message to the WebSocket client
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'create_date': event['create_date']
        }))

    @sync_to_async
    def save_message(self, user, room_name, message):
        # Save message to the database
        chat_group = currentChat.objects.get(unique_id=room_name)
        new_message = Conversation.objects.create(AuthorOfTheMessage=user, Message=message, create_date=timezone.now())
        chat_group.currentMessage.add(new_message)

    @sync_to_async
    def get_previous_messages(self, room_name):
        # Retrieve the last 50 messages from the database for the current chat room
        return Conversation.objects.filter(currentchat__unique_id=room_name).values(
            'Message', 'AuthorOfTheMessage__username', 'create_date'
        ).order_by('-create_date')[:50][::-1]  # Fetch the last 50 messages and reverse the order
