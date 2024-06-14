#Auth/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

DEFAULT_IMAGE = 'Auth/defaultAssets/ProfilePicture.png'

def upload_to(instance, filename):
    # Save the image in a subdirectory of MEDIA_ROOT
    # return '{instance}/{filename}'.format(filename=filename)
    return 'Auth/{instance}/{filename}'.format(filename=filename)

class MyUser(AbstractUser):
    profile_picture = models.ImageField(upload_to=upload_to, default=DEFAULT_IMAGE)
    about_me = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    friendlist = models.ManyToManyField('self', blank=True)
    
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
