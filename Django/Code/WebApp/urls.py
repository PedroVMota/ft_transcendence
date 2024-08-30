from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('Menu/', views.Menu, name='Menu'),
    path('Login/', views.login_register_view, name='Login'),
    path('Logout/', views.logout, name='Logout'),
    path('getUserData/', views.getUserData, name='getUserData'),
    # path('friendsList/', views.friends, name='friends'),
    #  const searchQuery = `/searchUser?user_code=${encodeURIComponent(userCode)}`;
    path('searchUser/', views.searchUser, name='searchUser'),
    path('Profile/', views.edit_profile, name='Profile'),
    path('Friends/', views.Friends, name='Friends'),

    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('get_friend_requests/', views.get_friend_requests, name='get_friend_requests'),
    path('manage_friend_request/', views.manage_friend_request, name='manage_friend_request'),
    

] 



