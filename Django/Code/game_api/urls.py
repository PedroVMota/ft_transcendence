from django.urls import path, include
from . import views


#Url Prefix: game/
#example: game/generate/
urlpatterns = [
    path('generate/', views.generate, name='generate'),
    path('join/', views.join_game, name='join_game'),
    path('leave/', views.leave_game, name='leave_game'),
    path('get/', views.get, name='get'),
] 
