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
    return random.randint(min, max)


class TrasationTable(models.Model):
    TYPE = (
        ('Deposit', 'Deposit'),
        ('Transfer', 'Transfer'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE)


    def __str__(self):
        return self.uuid
    
    def getDict(self):
        return {
            'uuid': self.uuid,
            'amount': self.amount,
            'type': self.type,
            'Description': self.Description
        }


class UserWallet(models.Model):
    User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    TransactionsHistory = models.ManyToManyField(TrasationTable, blank=True)

    def makeTransaction(self, amount: int, type: str, description: str) -> TrasationTable:
        if type == 'Deposit':
            self.balance += amount
        elif type == 'Transfer':
            self.balance -= amount
        else:
            raise ValueError("Invalid Transaction Type")
        self.save()
        transaction = TrasationTable.objects.create(amount=amount, type=type, Description=description)
        self.TransactionsHistory.add(transaction)
        self.save()
        return transaction
    
    def getTransactions(self):
        return [transaction.getDict() for transaction in self.TransactionsHistory.all()]
    
    def getBalance(self):
        return self.balance
    
    def __str__(self):
        return f"{self.User.username} Wallet"






class MyUser(AbstractUser):
    profile_picture = models.ImageField(upload_to=upload_to, default=DEFAULT_IMAGE)
    profile_banner = models.ImageField(upload_to=upload_to, default=DEFAULT_BANNER)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    userSocialCode = models.BigIntegerField(unique=True, null=True, blank=True)
    Wallet = models.OneToOneField(UserWallet, on_delete=models.CASCADE, null=True, blank=True)

    friendlist = models.ManyToManyField('self', blank=True)
    allChat = models.ManyToManyField(currentChat, blank=True)

    create_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, unique=False, null=True)


    #Statistics About the User
    TotalOfGames = models.IntegerField(default=0)
    NumberOfWins = models.IntegerField(default=0)
    NumberOfLosses = models.IntegerField(default=0)

    MMR = models.IntegerField(default=1) # Match Making Rank




    HigherRank = models.IntegerField(default=1) # The Highest Rank the user has ever reached
    DateOfHigherRank = models.DateTimeField(auto_now_add=True) # The Date the user reached the highest rank

    # AllPlayedGames = 
    def __add__user__(self, friend: 'MyUser'):
        """Add a user to the friend list."""
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
            },
            "Chats": self.getChatData(),
        }
    
    def save(self, *args, **kwargs):
        if self.userSocialCode is None:
            self.userSocialCode = RandomNumber(min=1000, max=9999)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username