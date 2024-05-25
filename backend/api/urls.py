from django.urls import path
from django.contrib import admin

from . import views
urlpatterns = [
    path('reg', views.regis, name='register'),
    path('log', views.log, name='register'),
]