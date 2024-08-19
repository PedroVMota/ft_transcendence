from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import path, include
from . import views


urlpatterns = [
    path('token/login/', views.UserLoginAPIView.as_view(), name='login'),
    path('token/register/', views.UserRegistrationView.as_view(), name='register'),
    path('token/flush/', views.CloseSession.as_view(), name='token_flush'),
    path('user/', views.UserDetailView.as_view(), name='user'),
    path('', views.HomeView.as_view(), name='home'),
]

