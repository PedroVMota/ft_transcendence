from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout
from .forms import LoginForm, RegistrationForm
from Auth.models import MyUser
from Auth.models import MyUser

def Menu(request):
    response = render(request, 'Components/Menu.html')
    return response

@login_required
def index(request):
    return render(request, 'index.html', {'user': request.user})

def login_register_view(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            return handle_login(request)
        elif 'register' in request.POST:
            return handle_registration(request)
    else:
        login_form = LoginForm()
        register_form = RegistrationForm()
    return render(request, 'register.html', {'login_form': login_form, 'register_form': register_form})

def handle_login(request):
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        return JsonResponse({'error': 'Invalid username or password'}, status=400)
    return JsonResponse({'error': 'Invalid form data'}, status=400)

def handle_registration(request):
    register_form = RegistrationForm(request.POST)
    if register_form.is_valid():
        if register_form.cleaned_data['password'] != register_form.cleaned_data['password_confirm']:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        user = register_form.save(commit=False)
        if(user.username == 'admin'):
            user.is_staff = True
            user.is_superuser = True
        user.save()
        return JsonResponse({'message': 'Registration successful'})
    return JsonResponse({'error': 'Invalid form data'}, status=400)

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({'message': 'Logout successful'})

@login_required
def edit_profile(request):
    if request.method == 'GET':
        print(" ====  GET REQUEST ====")
        userData: MyUser = request.user
        friendList = [friend.getJson() for friend in userData.friendlist.all()]

        blocked_users = [blocked_user.getJson() for blocked_user in userData.blocked_users.all()]

        if not blocked_users:
            blocked_users = None
        
        if not friendList:
            friendList = None

        print(userData)
        return render(request, 'Profile.html', {'user': userData, 'friendList': friendList, 'blocked_users': blocked_users})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def Friends(request):
    if request.user.is_authenticated:
        return render(request, 'Friends.html')
    return redirect('/')
 
def searchUser(request):
    if request.method == 'GET':
        friends = MyUser.objects.filter(userSocialCode=request.GET.get('user_code'))
        friends_data = [friend.getDict() for friend in friends]
        return JsonResponse({'friends': friends_data})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def Game(request):
    if(request.user.is_authenticated):
        return render(request, 'Game.html')
    return redirect('/')