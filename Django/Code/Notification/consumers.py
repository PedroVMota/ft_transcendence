# Sockets/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from Chat.models import Conversation, currentChat
from channels.db import database_sync_to_async
from django.utils import timezone

class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            print("User is anonymous")
            await self.close()
        else:
            self.group_name = f"user_{user.userSocialCode}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            print(f"User: ", user, "Connected!")
            await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the group
        print("User Disconnect");
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def Notification(self, event):
        # Send notification data to the WebSocket
        await self.send(text_data=json.dumps({
            'notifications': event['notifications']
        }))