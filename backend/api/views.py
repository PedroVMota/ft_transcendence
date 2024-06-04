from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseForbidden, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PongGameHistory, MyUser
import json
from django.contrib.auth import authenticate, login, logout as auth_logout
import os, sys


from django.contrib.auth import get_user_model

User = get_user_model()

""" JSON REQUEST REGISTER BODY:
{
    "username": "Admin",
    "password": "admin",
    "email": "newuser@example.com",
    "is_staff": true, //optional
    "is_superuser": true, //optional
    "is_active": true //optional
}

    JSON REQUEST LOGIN BODY:
{
    "username": "Admin",
    "password": "admin"
}

"""

from django.http import HttpResponseRedirect

def getProfilePicture(request, username=None):
    if username is None:
        user = request.user
        if user.is_anonymous:
            return  JsonResponse({"error": "User is not logged in"}, status=404)
    else:
        user = MyUser.objects.filter(username=username).first()
        if not user:
            raise Http404("User not found")
    print("THE LOGGED USER IS: ", user.username)
    if user.profile_image:
        path = os.getcwd() + user.profile_image.url
        print(path)
        if os.path.exists(path=path):
            return FileResponse(open(path, 'rb'))
        else:
            return JsonResponse({}, status=404)
    else:
        return JsonResponse({}, status=404)



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
            is_active = data.get('is_active', True)
            if not username or not password or not email:
                return JsonResponse({'error': 'Please provide username, password, and email'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            user = MyUser.objects.create_user(
                username=username,
                email=email,
            )
            user.set_password(password)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.is_active = is_active
            
            print(json.dumps({
                "username": user.get_username(),
                "email": user.email,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "is_active": user.is_active
            }, indent=4))
            user.save()
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def log(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        user = authenticate(request, username=username, password=password)
        if(user is not None):
            login(request, user)
            if user.is_active == False:
                return JsonResponse({"error": "User is suspended"}, status=400)
            response_data = {
                "Username": user.get_username(),
                "Email": user.email,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "Headers": dict(request.headers)
            }
            response = JsonResponse(response_data, status=200)
            return response
        else:
            return JsonResponse({"error": "Username or password is incorrect"}, status=400)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)


@csrf_exempt
def logout(request):
    if request.method == 'GET':
        return HttpResponseForbidden('Forbidden')
    if request.method == "POST":
        auth_logout(request)
        return JsonResponse({"message": "Logged out successfully"}, status=200)


@csrf_exempt
def get(requests):
    users = User.objects.all()
    response = []
    for user in users:
        response += [user.jsonInformation()]
    return JsonResponse(response, safe=False, status=200)


def getUserDetails(request):
    user = request.user
    if user.is_anonymous:
        return JsonResponse({"error": "User is not logged in"}, status=404)
    return JsonResponse(user.jsonInformation(), status=200)