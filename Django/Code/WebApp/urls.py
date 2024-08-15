from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('home/', views.home, name='Home'),
    path('login/', views.login, name='Login'),
    path('register/', views.register, name='Register'),
    path('logout/', views.logout, name='Logout'),
    path('profile/', views.Profile, name='Profile'),
] 

