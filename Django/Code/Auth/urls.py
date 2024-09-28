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





    # Friends Management
    path('token/block/<int:socialCode>/', views.block_user, name='block_user'),
    path('token/remove/<int:socialCode>/', views.remove, name='block_user'),

    
    path('', include('Notification.urls')),
    path('', include('Chat.urls')),
    


]
