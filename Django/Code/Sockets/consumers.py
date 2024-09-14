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
        # Get the room name from the URL route
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'pong_{self.room_name}'

        # Add the WebSocket connection to the group (room)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Load the received text data into a Python dictionary
        data = json.loads(text_data)

        # Print the received data from the client
        print("Received Data from client: ", json.dumps(data, indent=4))

        # Broadcast the received data to all users in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_update',  # This will trigger the game_update method for all clients
                'data': data  # Send the data received from the client to the room
            }
        )

    async def game_update(self, event):
        # Extract the data that was sent by the client
        received_data = event['data']

        # Print the event data for debugging
        print("Broadcasted Event Data: ", json.dumps(received_data, indent=4))

        # Game event, representing the updated game state (this can be dynamic in a real game)
        GameEvent: dict = {
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
                "GameRunning": True
            }
        }
        # Combine the received data from the client and the game event
        combined_data = {
            "ClientData": received_data,  # Data received from the client
            "GameEvent": GameEvent  # Static or dynamically updated game state
        }
        # Print the data before sending it to the client
        print("Sending to client: ", json.dumps(combined_data, indent=4))
        # Send the combined data (received input and the game event) back to the client
        await self.send(text_data=json.dumps(combined_data))

class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        # print("WebSocket connection accepted")
        # print(f"User: {user.username} and Code: {user.userSocialCode}")
        if user.is_anonymous:
            await self.close()
        else:
            # Group the user by their userSocialCode
            self.group_name = f"user_{user.userSocialCode}"
            # print("Group Name: ", self.group_name)
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
