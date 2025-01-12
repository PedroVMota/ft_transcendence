#Auth/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

notificationType = (
    ('friend_request', 'Friend Request'),
    ('lobby_invite', 'Lobby Invite'),
)

class FriendRequest(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=notificationType, default='friend_request')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    urlLobby = models.CharField(max_length=1024, null=True)
    noti = models.ForeignKey('Notification', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.from_user.username} sent a friend request to {self.to_user.username}"



notificationType = (
    ('friend_request', 'Friend Request'),
    ('lobby_invite', 'Lobby Invite'),
)
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=notificationType, default='friend_request')
    
    message = models.CharField(max_length=255)
    url = models.CharField(max_length=1024, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    fr = models.ForeignKey(FriendRequest, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"