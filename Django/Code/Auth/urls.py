from django.urls import path, include
from . import views





urlpatterns = [
    path('token/login/', views.UserLoginAPIView.as_view(), name='login'),
    path('token/register/', views.UserRegistrationView.as_view(), name='register'),
    path('token/flush/', views.CloseSession.as_view(), name='token_flush'),





    # Getters of information about the authjenticated user
    path('token/user/', views.user_data, name='user_data'),
    path('token/user/update/', views.update_user, name='update_user'),
    path('token/block_list/', views.block_list, name='block_list'),
    path('token/chat_details/', views.FriendChat, name='friend_list'),


    # Friends Management
    path('token/block/<int:socialCode>/', views.block_user, name='block_user'),
    path('token/remove/<int:socialCode>/', views.remove, name='block_user'),


    # path('token/request', views.request_reset, name='request_reset'),
    path('token/friend/request/get/', views.get_request, name='get_reset'),
    path('token/friend/request/manage/', views.manage_request, name='manage_reset'),
    path('token/friend/request/send/', views.send_request, name='send_reset'),

    path('token/notification/', views.get_notifications, name='get_notifications'),

]
