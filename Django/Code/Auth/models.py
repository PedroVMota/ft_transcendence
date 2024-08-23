#Auth/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

DEFAULT_IMAGE = 'Auth/defaultAssets/ProfilePicture.png'

def upload_to(instance, filename):
    # Save the image in a subdirectory of MEDIA_ROOT
    return 'Auth/{}/{}'.format(instance.username, filename)

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)  # Used for group chats
    is_group = models.BooleanField(default=False)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        if self.is_group:
            return self.name or 'Group Chat'
        else:
            return 'Chat between ' + ' & '.join([user.username for user in self.participants.all()])


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
    class Meta:
        ordering = ('-timestamp',)

class MyUser(AbstractUser):
    
    profile_picture = models.ImageField(upload_to=upload_to, default=DEFAULT_IMAGE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    friendlist = models.ManyToManyField('self', blank=True)
    darkMode = models.BooleanField(default=False)
    
    def getJson(self):
        return {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile_picture': self.profile_picture.url,
            'about_me': self.about_me,
            'create_date': self.create_date,
            'update_date': self.update_date,
            'friendlist': self.friendlist
        }
    
    def save(self, *args, **kwargs):
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
    status = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
