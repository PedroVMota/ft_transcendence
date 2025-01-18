from django.urls import path, include
from . import views





urlpatterns = [
    path('intra/', views.intra_auth, name='intra_auth'),
    path('initiate-oauth/', views.initiate_oauth, name='initiate_oauth'), 
    path('token/login/', views.UserLoginAPIView.as_view(), name='login'),
    path('token/register/', views.UserRegistrationView.as_view(), name='register'),
    path('token/flush/', views.CloseSession.as_view(), name='token_flush'),


    # Getters of information about the authjenticated user
    path('token/user/update/', views.update_user, name='update_user'),

    # Friends Management
    path('token/remove/<int:socialCode>/', views.remove, name='remove'),

    
    path('', include('Notification.urls')),
    path('', include('Chat.urls')),
    


]
