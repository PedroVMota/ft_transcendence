from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('Menu/', views.Menu, name='Menu'),
    path('Login/', views.login_register_view, name='Login'),
    path('Logout/', views.logout, name='Logout'),
    path('Profile/', views.edit_profile, name='Profile'),
    path('Friends/', views.Friends, name='Friends'),
] 



