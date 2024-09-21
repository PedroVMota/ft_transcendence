from django.contrib.auth import login
from django.utils import timezone
from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout
from WebApp.forms import LoginForm
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
import json




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