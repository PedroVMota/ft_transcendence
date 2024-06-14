from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import path, include
from .views import HomeView, UserDetailView, closeSession, UserRegistrationView, UserLoginView


urlpatterns = [
    path('token/login/', UserLoginView.as_view(), name='login'),
    path('token/register/', UserRegistrationView.as_view(), name='register'),
    path('token/flush/', closeSession.as_view(), name='token_flush'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Add this line
    path('user/', UserDetailView.as_view(), name='user'),
    path('', HomeView.as_view(), name='home'),
]

