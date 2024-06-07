from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class MyUser(AbstractUser):
    about_me = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    friendlist = models.ManyToManyField('self', blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
