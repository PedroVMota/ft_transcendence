from django.urls import path, re_path
from . import views
from Game import views as GameViews
from Lobby import views as LobbyViews


urlpatterns = [
    path('', views.index, name='Home'),
    path('Menu/', views.Menu, name='Menu'),
    path('Login/', views.login_register_view, name='Login'),
    path('Logout/', views.logout, name='Logout'),
    path('searchUser/', views.searchUser, name='searchUser'),
    re_path(r'^Profile/(?:(?P<socialCode>\d+)/)?$', views.Profile, name='Profile'),  # Make socialCode optional
    path('Friends/', views.Friends, name='Friends'),
    path('Game/', views.Game, name='Game'),
    #re_path(r'^Lobby/(?:(?P<lobby_id>\d+)/)?$', GameViews.MyLobby, name='Lobby'),

    path("Lobby/api/game/get/", GameViews.getGame, name='createGame'),
    path("Lobby/api/lobby/leave/", GameViews.leave_lobby, name='createGame'),
    path("Game/<str:game_id>/", GameViews.MyGame, name='Game'),

    path("Lobby/<str:lobby_id>", LobbyViews.MyLobby, name='Lobby'),
] 
