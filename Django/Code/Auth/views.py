from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import View
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
import json
from Auth.models import MyUser
from django.contrib.auth.decorators import login_required
from utils import shell_colors

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print(f"{shell_colors['BRIGHT_YELLOW']}Received login request for user: {username}{shell_colors['RESET']}")
            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)
            print(f"{shell_colors['BRIGHT_GREEN']}Attempting to authenticate user: {username}{shell_colors['RESET']}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(f"{shell_colors['BRIGHT_GREEN']}User {username} authenticated successfully{shell_colors['RESET']}")
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                print(f"{shell_colors['BRIGHT_RED']}Invalid username or password{shell_colors['RESET']}")
                return JsonResponse({'error': 'Invalid username or password'}, status=400)
        except json.JSONDecodeError:
            print(f"{shell_colors['BRIGHT_RED']}Invalid JSON data received{shell_colors['RESET']}")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(f"{shell_colors['BRIGHT_RED']}Unhandled exception: {e}{shell_colors['RESET']}")
            return JsonResponse({'error': str(e)}, status=500)
    def get(self, request):
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token})
    
@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(View):
    def post(self, request):
        User = get_user_model()
        try:
            data = json.loads(request.body)
            print(f"{shell_colors['BRIGHT_YELLOW']}Received registration request{shell_colors['RESET']}")
            username = data.get('username')
            password = data.get('password')
            password_confirm = data.get('password2')
            print(f"{shell_colors['BRIGHT_GREEN']}Attempting to register user: {username}{shell_colors['RESET']}")
            if not username or not password:
                print(f"{shell_colors['BRIGHT_RED']}Validation Error: All fields are required{shell_colors['RESET']}")  # Log validation failure
                return JsonResponse({'error': 'All fields are required'}, status=400)
            if password != password_confirm:
                print(f"{shell_colors['BRIGHT_RED']}Validation Error: Passwords do not match{shell_colors['RESET']}")  # Log validation failure
                return JsonResponse({'error': 'Passwords do not match'}, status=400)
            if User.objects.filter(username=username).exists():
                print(f"{shell_colors['BRIGHT_RED']}Validation Error: Username already exists{shell_colors['RESET']}")
                return JsonResponse({'error': 'Username already exists'}, status=400)
            print(f"{shell_colors['BRIGHT_GREEN']}Creating user: {username}{shell_colors['RESET']}")
            if ' ' in username:
                first, last = username.split(' ', 1)  # Split on first space only
            else:
                first = last = username  # Use username as both first and last name

            print(f"{shell_colors['BRIGHT_GREEN']}User {username} created successfully{shell_colors['RESET']}")
            # Create the user (email can be None)
            user = User.objects.create(
                username=username,
                password=make_password(password),
                first_name=first,
                last_name=last,
            )
            return JsonResponse({'message': 'Registration successful'}, status=201)
        except json.JSONDecodeError:
            print(f"{shell_colors['BRIGHT_RED']}Invalid JSON data received{shell_colors['RESET']}")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"{shell_colors['BRIGHT_RED']}Unhandled exception: {e}{shell_colors['RESET']}")
            return JsonResponse({'error': str(e)}, status=500)
    
@method_decorator(csrf_exempt, name='dispatch')
class CloseSession(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'Session closed'})
        else:
            return Response({'message': 'No active session'})


@login_required
def update_user(request):
    print(request.method)
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)
    user = request.user
    print(f"{shell_colors['BRIGHT_YELLOW']}Updating user: {user.username}{shell_colors['RESET']}")
    if 'profile_picture' in request.FILES:
        user.profile_picture = request.FILES['profile_picture']
    if 'profile_banner' in request.FILES:
        user.profile_banner = request.FILES['profile_banner']
    if 'first_name' in request.POST and request.POST['first_name']:
        user.first_name = request.POST['first_name']
    if 'last_name' in request.POST and request.POST['last_name']:
        user.last_name = request.POST['last_name']
    print(f"{shell_colors['BRIGHT_GREEN']}User {user.username} updated successfully{shell_colors['RESET']}")
    try:
        print(f"{shell_colors['BRIGHT_GREEN']}Saving user: {user.username}{shell_colors['RESET']}")
        user.save()  # Save only after checking all fields
        return JsonResponse({'message': 'User updated successfully.'}, status=200)
    except Exception as e:
        print(f"{shell_colors['BRIGHT_RED']}Failed to update user. Reason: {e}{shell_colors['RESET']}")
        return JsonResponse({'error': f'Failed to update user. Reason: {e}'}, status=500)

    
def remove(request, socialCode):
    if request.method == "POST":
        user: MyUser = request.user
        print(f"{shell_colors['BRIGHT_YELLOW']}Removing friend with social code: {socialCode}{shell_colors['RESET']}")
        friend_to_remove = MyUser.objects.get(userSocialCode=socialCode)
        print(f"{shell_colors['BRIGHT_GREEN']}Removing friend {friend_to_remove.username}{shell_colors['RESET']}")
        user.removeFriend(friend_to_remove)
        print(f"{shell_colors['BRIGHT_GREEN']}Friend {friend_to_remove.username} removed successfully{shell_colors['RESET']}")
        return JsonResponse({'status': 'success', 'message': f'Friend {friend_to_remove.username} removed successfully.'})
