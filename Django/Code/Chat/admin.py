from django.contrib import admin
from .models import Conversation, currentChat

# Register your models here
admin.site.register(Conversation)
admin.site.register(currentChat)
