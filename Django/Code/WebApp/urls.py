from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('home/', views.home, name='Home'),
    path('login/', views.Auth, name='Login'),
    path('register/', views.Auth, name='Register'),
    path('Logout/', views.logout, name='Logout'),
    path('Profile/', views.Profile, name='Profile'),
] 

