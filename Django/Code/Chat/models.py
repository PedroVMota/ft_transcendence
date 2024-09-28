from django.db import models
from django.conf import settings
import uuid

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    AuthorOfTheMessage = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='AuthorOfTheMessage')
    Message = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_user_conversations(user):
        """Get all conversations excluding those involving blocked users."""
        blocked_users = user.blocked_users.all()
        return Conversation.objects.filter(
            currentchat__members=user
        ).exclude(
            currentchat__members__in=blocked_users
        ).distinct()
    
    def getDict(self):
        return {
            'Author': self.AuthorOfTheMessage.username,
            'Message': self.Message,
            'Date': self.create_date
        }

    def __str__(self):
        return f"Conversation {self.id}"

class currentChat(models.Model):
    id = models.AutoField(primary_key=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    is_active = models.BooleanField(default=True)
    is_group = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    currentMessage = models.ManyToManyField(Conversation, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)  # Remove unique=True for now

    def getDict(self):
        return {
            'ChatId': str(self.unique_id),
            'Members': [member.username for member in self.members.all()],
            'Messages': [message.getDict() for message in self.currentMessage.all()]
        }

    def __str__(self):
        return f"Conversation {self.id}"