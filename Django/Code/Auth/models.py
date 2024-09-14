#Auth/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
import random
import os

# Create your models here.

DEFAULT_IMAGE = 'Auth/defaultAssets/ProfilePicture.png'

def upload_to(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = f'profile_{instance.username}.{extension}'
    return os.path.join('Auth', instance.username, new_filename)


def RandomNumber(min=1000, max=9999):
    return random.randint(min, max)

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    AuthorOfTheMessage = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='AuthorOfTheMessage')
    Message = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"



class currentChat(models.Model):
    id = models.AutoField(primary_key=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    is_group = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    currentMessage = models.ManyToManyField(Conversation, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)  # Remove unique=True for now

    def __str__(self):
        return f"Conversation {self.id}"
    
USERSTATES = (
    (1, 'Online'),
    (2, 'Offline'),
)

class MyUser(AbstractUser):
    profile_picture = models.ImageField(upload_to=upload_to, default=DEFAULT_IMAGE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    friendlist = models.ManyToManyField('self', blank=True)
    userSocialCode = models.BigIntegerField(unique=True, null=True, blank=True)
    allChat = models.ManyToManyField(currentChat, blank=True)
    state = models.IntegerField(choices=USERSTATES, default=2)
    walletCoins = models.IntegerField(default=0)
    
    def getJson(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'usercode': self.userSocialCode,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile_picture': self.profile_picture.url,
            'about_me': self.about_me,
            'create_date': self.create_date,
            'update_date': self.update_date,
            'friendlist': [friend.username for friend in self.friendlist.all()]
        }
    
    def save(self, *args, **kwargs):
        if self.userSocialCode is None:
            self.userSocialCode = RandomNumber(min=1000, max=9999)
        super().save(*args, **kwargs)

    def newImageUpdate(self, image):
        self.profile_picture = image
        self.save()

    def __str__(self):
        return self.username
    

class serverLogs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    mehod = models.CharField(max_length=10, default='GET')
    path = models.CharField(max_length=100, default='/')
    status = models.BigIntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username




class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    def __str__(self):
        return f"{self.from_user.username} sent a friend request to {self.to_user.username}"



class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
