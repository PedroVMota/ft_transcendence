from django.urls import path, include
from . import views





urlpatterns = [
    path('token/chat_details/', views.FriendChat, name='friend_list'),
]
