from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from Chat.models import currentChat
import uuid
import random
import os


DEFAULT_IMAGE = 'Auth/defaultAssets/ProfilePicture.png'
DEFAULT_BANNER = 'Auth/defaultAssets/ProfileBanner.png'

def upload_to(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = f'profile_{instance.username}.{extension}'
    return os.path.join('Auth', instance.username, new_filename)


def RandomNumber(min=1000, max=9999):
    print("RandomNumber")
    return random.randint(min, max)

def generate_random_color():
    """Gera uma cor aleatória no formato hexadecimal"""
    return f"#{random.randint(0, 0xFFFFFF):06x}"
class MyUser(AbstractUser):
    intraCode = models.CharField(max_length=2048, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=upload_to, default=DEFAULT_IMAGE)
    profile_banner = models.ImageField(upload_to=upload_to, default=DEFAULT_BANNER)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    userSocialCode = models.BigIntegerField(unique=True, null=True, blank=True)
    friendlist = models.ManyToManyField('self', blank=True)
    allChat = models.ManyToManyField(currentChat, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, unique=False, null=True)
    TotalOfGames = models.IntegerField(default=0)
    NumberOfWins = models.IntegerField(default=0)
    NumberOfLosses = models.IntegerField(default=0)
    MMR = models.IntegerField(default=1)
    HigherRank = models.IntegerField(default=1)
    DateOfHigherRank = models.DateTimeField(auto_now_add=True)
    paddle_color = models.CharField(max_length=7, default=generate_random_color)

    # AllPlayedGames = 
    def __add__user__(self, friend: 'MyUser'):
        if friend in self.friendlist.all():
            raise ValueError("User is already a friend")
        if friend == self:
            raise ValueError("User cannot add themselves as a friend")
        self.friendlist.add(friend)
        chat: currentChat = currentChat.objects.create()
        chat.members.add(self)
        chat.members.add(friend)
        self.allChat.add(chat)
        self.save()
        
    def removeFriend(self, user: 'MyUser'):
        if user not in self.friendlist.all():
            pass
        else:
            self.friendlist.remove(user)
            chats: currentChat = currentChat.objects.filter(members=user).filter(members=self)
            for chat in chats:
                chat.delete()
            self.save()
        self.allChat.filter(members=user).delete()
    
    def isFriend(self, user: 'MyUser'):
        for friend in self.friendlist.all():
            if friend == user:
                return True
        return False


    def getChatData(self):
        return [chat.getDict() for chat in self.allChat.all()]

    def getFriendList(self):
        return [friend.username for friend in self.friendlist.all()]

    def allChats(self):
        return [chat.unique_id for chat in self.allChat.all()]
    

    def getDict(self):
        return {
            "Info": {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'userCode': self.userSocialCode,
                "profile_picture": self.profile_picture.url,
                "profile_banner": self.profile_banner.url,
                "paddle_color": self.paddle_color,
            },
            "Chats": self.getChatData(),
        }
    
    def save(self, *args, **kwargs):
        if self.userSocialCode is None:
            self.userSocialCode = RandomNumber(min=1000, max=9999)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username