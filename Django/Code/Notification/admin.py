from django.contrib import admin
from .models import FriendRequest, Notification
# Register your models here.

admin.site.register(FriendRequest)
admin.site.register(Notification)
    