from django.urls import path, include
from . import views


#example: /Game/
urlpatterns = [
    path('api/lobby/create/', views.createLobby), # Create a lobby
    path('api/lobby/information/', views.getLobbyInformation), # Get the information of the lobby
] 
