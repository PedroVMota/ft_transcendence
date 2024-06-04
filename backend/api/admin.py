from django.contrib import admin




from .models import MyUser, PongGameHistory


admin.site.register(MyUser)
admin.site.register(PongGameHistory)
# Register your models here.
