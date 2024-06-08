#Auth/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

DEFAULT_IMAGE = 'Auth/defaultAssets/ProfilePicture.png'

def upload_to(instance, filename):
    print('instance', instance)
    return 'images/{filename}'.format(filename=filename)

class MyUser(AbstractUser):
    profile_picture = models.ImageField(upload_to=upload_to, default=DEFAULT_IMAGE)
    about_me = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    friendlist = models.ManyToManyField('self', blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
