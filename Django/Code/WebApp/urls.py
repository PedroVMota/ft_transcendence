from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('Menu/', views.Menu, name='Menu'),
    path('Login/', views.login_register_view, name='Login'),
    path('Logout/', views.logout, name='Logout'),
    path('searchUser/', views.searchUser, name='searchUser'),
    re_path(r'^Profile/(?:(?P<socialCode>\d+)/)?$', views.Profile, name='Profile'),  # Make socialCode optional
    path('Friends/', views.Friends, name='Friends'),
    path('Game/', views.Game, name='Game'),
] 
