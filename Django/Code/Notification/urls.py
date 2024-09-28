from django.urls import path, include
from . import views





urlpatterns = [
    path('token/friend/request/get/', views.get_request, name='get_reset'),
    path('token/friend/request/manage/', views.manage_request, name='manage_reset'),
    path('token/friend/request/send/', views.send_request, name='send_reset'),
    path('token/notification/', views.get_notifications, name='get_notifications'),
]
