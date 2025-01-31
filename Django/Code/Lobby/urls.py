from Game.urls import urlpatterns
from . import views

from django.urls import path

urlpatterns = [
    path('api/lobby/create', views.createLobby),
    path('api/lobby/information', views.getLobbyInformation),
]