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
from .forms import ProfileUpdateForm

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid username or password'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        # Returns the CSRF token for use in client-side requests
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token})
    
@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(View):
    def post(self, request):
        User = get_user_model()
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Log the received data
            username = data.get('username')
            password = data.get('password')
            password_confirm = data.get('password2')

            if not username or not password:
                print("Validation Error: Missing fields")  # Log validation failure
                return JsonResponse({'error': 'All fields are required'}, status=400)
            if password != password_confirm:
                print("Validation Error: Passwords do not match")  # Log validation failure
                return JsonResponse({'error': 'Passwords do not match'}, status=400)
            if User.objects.filter(username=username).exists():
                print("Validation Error: Username already exists")  # Log validation failure
                return JsonResponse({'error': 'Username already exists'}, status=400)
            
            # Split username into first and last name if it contains a space
            if ' ' in username:
                first, last = username.split(' ', 1)  # Split on first space only
            else:
                first = last = username  # Use username as both first and last name

            # Create the user (email can be None)
            user = User.objects.create(
                username=username,
                password=make_password(password),
                first_name=first,
                last_name=last,
            )
            return JsonResponse({'message': 'Registration successful'}, status=201)
        except json.JSONDecodeError:
            print("Error: Invalid JSON received")  # Log JSON decode failure
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print("Unhandled Exception:", str(e))  # Log any other unhandled exceptions
            return JsonResponse({'error': str(e)}, status=500)
    
@method_decorator(csrf_exempt, name='dispatch')
class CloseSession(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'Session closed'})
        else:
            return Response({'message': 'No active session'})

def user_data(request):
    if request.user.is_authenticated:
        user: MyUser = request.user
        return JsonResponse(user.getDict(), status=200)
    else:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    


@login_required
def update_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)
    user = request.user
    if 'profile_picture' in request.FILES:
        user.profile_picture = request.FILES['profile_picture']
    if 'profile_banner' in request.FILES:
        user.profile_banner = request.FILES['profile_banner']
    if 'first_name' in request.POST and request.POST['first_name']:
        user.first_name = request.POST['first_name']
    if 'last_name' in request.POST and request.POST['last_name']:
        user.last_name = request.POST['last_name']
    try:
        user.save()  # Save only after checking all fields
        return JsonResponse({'message': 'User updated successfully.'}, status=200)
    except Exception as e:
        return JsonResponse({'error': f'Failed to update user. Reason: {e}'}, status=500)

def block_list(request):
    if request.user.is_authenticated:
        user: MyUser = request.user
        return JsonResponse(user.getBlockedUsers(), status=200)
    else:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
def block_user(request, socialCode):
    """View to block a user."""
    if request.method == "POST":
        user: MyUser = request.user
        targetUser = MyUser.objects.get(userSocialCode=socialCode)
        user.blockUser(targetUser)
        return JsonResponse({'status': 'success', 'message': f'User {targetUser.username} blocked successfully.'})

def remove(request, user_id):
    if request.method == "POST":
        user: MyUser = request.user
        friend_to_remove = MyUser.objects.get(id=user_id)
        user.removeFriend(friend_to_remove)
        return JsonResponse({'status': 'success', 'message': f'Friend {friend_to_remove.username} removed successfully.'})
