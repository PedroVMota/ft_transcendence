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

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPIView(View):
    def post(self, request):
        try:
            # Parse the incoming JSON body
            body = json.loads(request.body)

            # Extract username and password from the data object
            username = body.get('username')
            password = body.get('password')

            print(f"{shell_colors['BRIGHT_YELLOW']}Received login request for user: {username}{shell_colors['RESET']}")

            # Check if both username and password are provided
            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            print(f"{shell_colors['BRIGHT_GREEN']}Attempting to authenticate user: {username}{shell_colors['RESET']}")

            # Attempt to authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                print(f"{shell_colors['BRIGHT_GREEN']}User {username} authenticated successfully{shell_colors['RESET']}")
                # Log the user in
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
        # Return the CSRF token for any GET request (for example, login form)
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token})

    
@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(View):
    def post(self, request):
        User = get_user_model()
        try:
            body = json.loads(request.body)
            username = body.get('username')
            first_name = body.get('first_name')
            last_name = body.get('last_name')
            password = body.get('password')

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
        print(f"User {user.username} updated successfully")
        return JsonResponse({'message': 'User updated successfully.'}, status=200)
    except Exception as e:
        print(f"Failed to update user. Reason: {e}")
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



from django.contrib.auth import login

def intra_auth(request):
    code = request.GET.get('code')
    if code:
        # Step 1: Exchange the authorization code for an access token
        oauth_url = 'https://api.intra.42.fr/oauth/token'
        
        INTRA_CLIENT_ID = "u-s4t2ud-6797340cf0815ac0286e74fb21bd6a3b9352ebf48cb8523c972b318e307f5be2"
        INTRA_CLIENT_SECRET = "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"
        INTRA_REDIRECT_URI = "https://localhost/auth/intra"

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

    # Make the API request to get user information
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
        print(response.status_code)
        print(response.json())
        return None
