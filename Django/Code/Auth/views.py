from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.views.generic import View
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
import json
from Auth.models import MyUser
from utils import shell_colors
import requests
import os
import string

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPIView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            username = body.get('username')
            password = body.get('password')
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
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token})

    
@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            username = body.get('username')
            first_name = body.get('first_name')
            last_name = body.get('last_name')
            password = body.get('password')
            if len(password) < 8 or (not any(char in string.punctuation for char in password) or not any(char.isdigit() for char in password)):
                return JsonResponse({'error': 'Password must contain at least 8 characters, a digit and a special character'}, status=400)
            if not username or not first_name or not last_name or not password:
                return JsonResponse({'error': 'All fields are required: username, first_name, last_name, password'}, status=400)
            # Hash the password before creating the user
            hashed_password = make_password(password)
            # Create and save the new user
            if(MyUser.objects.filter(username=username).exists()):
                # throw new Error(`Registration failed: ${response.status}`);
                return JsonResponse({'error': 'User already exists'}, status=400)
            new_user = MyUser.objects.create(
                username=username,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name
            )
            new_user.save()

            # Return success response
            return JsonResponse({'message': 'User created successfully'}, status=201)
        except json.JSONDecodeError:
            # Handle invalid JSON
            return JsonResponse({'error': 'Invalid JSON data received'}, status=400)
        except Exception as e:
            # Handle other exceptions
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
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)
    user = request.user
    print(f"Updating user: {user.username}")
    
    if 'profile_picture' in request.FILES:
        user.profile_picture = request.FILES['profile_picture']
    if 'profile_banner' in request.FILES:
        user.profile_banner = request.FILES['profile_banner']
    if 'first_name' in request.POST and request.POST['first_name']:
        user.first_name = request.POST['first_name']
    if 'last_name' in request.POST and request.POST['last_name']:
        user.last_name = request.POST['last_name']
    
    try:
        user.save()
        return JsonResponse({'message': 'User updated successfully.'}, status=200)
    except Exception as e:
        return JsonResponse({'error': f'Failed to update user. Reason: {e}'}, status=500)

    
def remove(request, socialCode):
    if request.method == "POST":
        user: MyUser = request.user
        friend_to_remove = MyUser.objects.get(userSocialCode=socialCode)
        user.removeFriend(friend_to_remove)
        return JsonResponse({'status': 'success', 'message': f'Friend {friend_to_remove.username} removed successfully.'})



from django.contrib.auth import login

def intra_auth(request):
    code = request.GET.get('code')
    if code:
        # Step 1: Exchange the authorization code for an access token
        oauth_url = 'https://api.intra.42.fr/oauth/token'
        INTRA_CLIENT_ID = os.environ.get('INTRA_CLIENT_ID')
        INTRA_CLIENT_SECRET = os.environ.get('INTRA_CLIENT_SECRET')
        INTRA_REDIRECT_URI = os.environ.get('INTRA_REDIRECT_URI')
        data = {
            'grant_type': 'authorization_code',
            'client_id': INTRA_CLIENT_ID,
            'client_secret': INTRA_CLIENT_SECRET,
            'code': code,
            'redirect_uri': INTRA_REDIRECT_URI
        }

        # Exchange the code for an access token
        response = requests.post(oauth_url, data=data)
        if response.status_code == 200:
            # Step 2: Extract access token from the response
            token_data = response.json()
            access_token = token_data.get('access_token')
            user_info = get_user_info(access_token)
            try:
                User: MyUser = MyUser.objects.get(username=user_info['username'])
            except MyUser.DoesNotExist:
                User = MyUser.objects.create(username=user_info['username'], first_name=user_info['first_name'], last_name=user_info['last_name'])
                User.save()
            # Specify the backend to avoid the ValueError
            backend_path = 'django.contrib.auth.backends.ModelBackend'
            User.backend = backend_path
            # Log the user in
            login(request, User, backend=backend_path)
            return redirect('/')
        else:
            print(response.status_code)
            print(response.json())
            return HttpResponse('Failed to authenticate user', status=500)
    else:
        return HttpResponse('No code provided', status=400)



def get_user_info(access_token):
    """Function to retrieve user information using the access token."""
    api_url = 'https://api.intra.42.fr/v2/me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(api_url, headers=headers)
    if(response.status_code == 200):
        content = response.json()
        relevantData = {
            'username': content['login'],
            'first_name': content['first_name'],
            'last_name': content['last_name'],
        }
        return relevantData
    else:
        return None

def initiate_oauth(request):
    client_id = os.environ.get('INTRA_CLIENT_ID')
    redirect_uri = os.environ.get('INTRA_REDIRECT_URI')
    oauth_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(oauth_url)