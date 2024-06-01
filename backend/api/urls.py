from django.urls import path
from django.contrib import admin

from . import views
urlpatterns = [
    path('register', views.regis, name='register'),
    path('login', views.log, name='login'),
    path('logout', views.logout, name='logout'),
    path('getUsers', views.get, name='getUsers')
]