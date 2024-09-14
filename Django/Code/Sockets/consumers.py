# Sockets/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json
from Auth.models import Conversation, currentChat
from channels.db import database_sync_to_async
from django.utils import timezone

"""
[
    {
        "PlayerOne": {
            "xPercent": 0.5
        },
        "PlayerTwo": {
            "xPercent": 0.5
        },
        "Ball": {
            "xPercent": 0.5,
            "yPercent": 0.5
        },
        "Score": {
            "PlayerOne": 0,
            "PlayerTwo": 0
        },
        "GameState": {
            "GameRunning": true
        }
    },
    {
        "GameEvent": {
            "PlayerOneScored": {
                "Event": [ "Up", "Down"]
            },
            "PlayerTwoScored": {
                "Event": [ "Up", "Down"]
            },
            "Event": [
                "PlayerOneScored",
                "PlayerTwoScored",
                "PlayerOneWon",
                "PlayerTwoWon",
                "GamePaused",
                "GameResumed"
            ]
        }
    }
]
"""

class PongGameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Get the room name from the URL route (passed in the websocket route)
        print("All The Scope: ", self.scope)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'pong_{self.room_name}'
        print(f"New connection: {self.channel_name} to room {self.room_group_name}")
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

        # You could send a message or acknowledge that the connection was successful
        await self.send(text_data=json.dumps({
            'message': f'You have connected to room {self.room_group_name}'
        }))

    async def disconnect(self, close_code):
        # Print disconnection information
        print(f"Disconnection: {self.channel_name} from room {self.room_group_name}")

        # Remove the WebSocket connection from the group (room)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data):
        # Load the received text data into a Python dictionary
        data = json.loads(text_data)

        # Print the data received from the client
        print("Received Data: ", json.dumps(data, indent=4))

        # Print the current channel name (which uniquely identifies the WebSocket connection)
        print(f"Sending to all users in channel group: {self.room_group_name}, current channel: {self.channel_name}")

        # Send the data to all users in the room group
        await self.channel_layer.group_send(
            self.room_group_name,  # The WebSocket room the users are part of
            {
                'type': 'game_update',  # The function name that will handle the event in each WebSocket
                'data': data  # The data to be sent to all clients in the room
            }
        )

    async def game_update(self, event):
        # This dictionary represents possible game events
        GameEvent: dict = {
            "PlayerOneScored": {
                "Event": ["Up", "Down"]
            },
            "PlayerTwoScored": {
                "Event": ["Up", "Down"]
            },
            "Event": [
                "PlayerOneScored",
                "PlayerTwoScored",
                "PlayerOneWon",
                "PlayerTwoWon",
                "GamePaused",
                "GameResumed"
            ]
        }
        # Print the GameEvent JSON before sending it
        print("Sending GameEvent to client:", json.dumps(GameEvent, indent=4))
        # Send only the GameEvent JSON to the WebSocket client
        await self.send(text_data=json.dumps(GameEvent))


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
    async def Notification(self, event):
        # Send notification data to the WebSocket
        await self.send(text_data=json.dumps({
            'notifications': event['notifications']
        }))


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
