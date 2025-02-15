# Sockets/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from Chat.models import Conversation, currentChat
from channels.db import database_sync_to_async
from django.utils import timezone
from utils import shell_colors


# Example usage:
class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            print(f"{shell_colors['BRIGHT_RED']}Anonymous User Disconnected{shell_colors['RESET']}")
            await self.close()
        else:
            self.group_name = f"user_{user.userSocialCode}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            print(f"{shell_colors['BRIGHT_GREEN']}{user} Connected{shell_colors['RESET']}")
            await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the group
        user = self.scope["user"]
        print(f"{shell_colors['BRIGHT_RED']}{user} Disconnected Code: {close_code}{shell_colors['RESET']}")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def Notification(self, event):
        # Send notification data to the WebSocket
        print(f"{shell_colors['BRIGHT_YELLOW']}Notification sent{shell_colors['RESET']}")
        print(json.dumps(event['notifications']))
        await self.send(text_data=json.dumps({
            'notifications': event['notifications']
        }))