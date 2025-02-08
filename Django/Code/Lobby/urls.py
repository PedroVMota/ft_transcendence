from Game.urls import urlpatterns
from . import views

from django.urls import path

urlpatterns = [
    path('create/', views.createLobby),
    path('information/', views.getLobbyInformation),
]