from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.contrib.auth import authenticate, login


""" JSON REQUEST REGISTER BODY:
{
    "username": "Admin",
    "password": "admin",
    "email": "newuser@example.com",
    "is_staff": true, //optional
    "is_superuser": true //optional
}

"""
@csrf_exempt
def regis(request):
    if request.method == 'GET':
        return HttpResponseForbidden('Forbidden')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            is_staff = data.get('is_staff', False)
            is_superuser = data.get('is_superuser', False)
            if not username or not password or not email:
                return JsonResponse({'error': 'Please provide username, password, and email'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            # Update the user with staff and superuser status if specified
            if is_staff:
                user.is_staff = True
            if is_superuser:
                user.is_superuser = True
                user.is_staff = True  # Superusers must also be staff
            user.save()
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

def log(request):
    print("============================================  LOGIIIIIIIIIIIIIIINN ============================================ ")
    if request.method == "POST":
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        user = authenticate(request, username=username, password=password)
        if(user is not None):
            login(request, user)
            response = {
                "Username": user.get_username(),
                # "csrf_exempt": request.META.get('HTTP_AUTHORIZATION')
            }
            return JsonResponse(response, status=200)
        else:
            return JsonResponse({"error": "Wrong Credentials"}, status=404)