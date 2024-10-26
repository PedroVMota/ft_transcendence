from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import MyUser
from utils import shell_colors

class UserLogin(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print(f"{shell_colors['BRIGHT_YELLOW']}Authentication from From user login: {username}{shell_colors['RESET']}")
            # Check if the user exists by username
            user = MyUser.objects.get(username=username)
            # Verify if the provided password matches the hashed password stored in the database
            if check_password(password, user.password):
                return user
            else:
                return None
        except MyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None