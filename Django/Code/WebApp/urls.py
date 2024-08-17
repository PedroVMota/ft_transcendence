from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('Menu/', views.Menu, name='Menu'),
    path('login/', views.Auth, name='Login'),
    path('register/', views.Auth, name='Register'),
    path('Logout/', views.logout, name='Logout'),
    path('Profile/', views.profile, name='Profile'),
    path('Friends/', views.Friends, name='Friends'),
] 



