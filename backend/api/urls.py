from django.urls import path
from django.contrib import admin

from . import views
urlpatterns = [
    path('register', views.regis, name='register'),
    path('login', views.log, name='login'),
    path('logout', views.logout, name='logout'),
    path('getUsers', views.get, name='getUsers'),
    path('pImg/<str:username>/', views.getProfilePicture, name='get_profile_picture'),
    path('pImg/', views.getProfilePicture, name='get_own_profile_picture'),
    # path('upload', views.upload_file, name='upload_file'),
    # path('getImages', views.getImages, name='getImages'),
]