from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('Menu/', views.Menu, name='Menu'),
    path('Login/', views.login_register_view, name='Login'),
    path('Logout/', views.logout, name='Logout'),
    path('getUserData/', views.getUserData, name='getUserData'),
    # path('friendsList/', views.friends, name='friends'),
    #  const searchQuery = `/searchUser?user_code=${encodeURIComponent(userCode)}`;
    path('searchUser/', views.searchUser, name='searchUser'),
    path('Profile/', views.edit_profile, name='Profile'),
    path('Friends/', views.Friends, name='Friends'),
    path('Game/', views.Game, name='Game'),
]
