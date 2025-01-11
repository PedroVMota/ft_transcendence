from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout
from .forms import LoginForm, RegistrationForm
from Auth.models import MyUser
from Notification.models import FriendRequest
import json
from utils import shell_colors
from Game.Forms import LobbyForm
from Game.models import Lobby

def Menu(request):
    response = render(request, 'Components/Menu.html')
    return response



@login_required
def index(request):
    print(" ====  INDEX REQUEST ====")
    user = request.user
    user_lobbies = Lobby.objects.filter(players=user)
    context = {'user': user}
    if user_lobbies.exists():
        print(" ====  LOBBY EXISTS ====")
        # The user is already in a lobby
        user_lobby = user_lobbies.first()
        lobby_data = user_lobby.getDict()
        context['lobby'] = lobby_data
        context['lobbyJson'] = json.dumps(lobby_data)
        # /Lobby/6f6aeb32-9b41-4b2c-be5d-1769f2c87628
        return redirect(f'/Lobby/{user_lobby.id}')

    else:
        print(" ====  LOBBY FORM ====")
        # The user is not in a lobby, include the forms
        lobby_form = LobbyForm()
        context['form'] = lobby_form

    return render(request, 'index.html', context)


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
def Profile(request, socialCode=None):
    if request.method == 'GET':
        print(" ====  GET REQUEST ====")
        
        try:
            userData = MyUser.objects.get(userSocialCode=socialCode)
        except MyUser.DoesNotExist:
            return render(request, 'Profile.html', {
                'user': request.user,
                'friendList': [friend.getDict() for friend in request.user.friendlist.all()],
                'can_edit': True,
                'friend_request_status': None
            })
        
        can_edit = (userData == request.user)
        
        friendList = [friend.getDict() for friend in userData.friendlist.all()]

        if not friendList:
            friendList = None

        # Check friend request status and friendship
        friend_request_status = None
        areTheyFriends = False

        if not can_edit:
            # Check if there's a pending or accepted friend request
            friend_request = FriendRequest.objects.filter(
                from_user=request.user, 
                to_user=userData
            ).filter(status__in=['pending', 'accepted']).first()

            if friend_request:
                # If there is a friend request, use its status
                friend_request_status = friend_request.status
                # If the friend request is accepted, mark them as friends
                if friend_request.status == 'accepted':
                    areTheyFriends = True
            else:
                # Check if they are friends by calling the isFriend method
                areTheyFriends = request.user.isFriend(userData)
                # If they are friends, set the status to 'accepted'
                if areTheyFriends:
                    friend_request_status = 'accepted'
                else:
                    # Otherwise, they are not friends and no friend request is pending
                    friend_request_status = 'rejected'

        print(f"{shell_colors['BRIGHT_YELLOW']}Friend Request Status: {friend_request_status}{shell_colors['RESET']}")

        if friend_request_status == 'accepted' and userData.isFriend(request.user):
            print(f"{shell_colors['BRIGHT_GREEN']}They are friends{shell_colors['RESET']}")
            friend_request_status = 'accepted'
        else:
            print(f"{shell_colors['BRIGHT_RED']}They are not friends{shell_colors['RESET']}")
            friend_request_status = 'rejected'
        return render(request, 'Profile.html', {
            'user': userData,
            'friendList': friendList,
            'can_edit': can_edit,
            'friend_request_status': friend_request_status
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

from Chat.models import currentChat
@login_required
def Friends(request):
    if request.user.is_authenticated:
        user: MyUser = request.user
        friendlist = user.friendlist.all()
        friends_data = []

        for friend in friendlist:
            friend_dict = friend.getDict()
            chats = currentChat.objects.filter(members=user).filter(members=friend)
            friend_dict['chats'] = [chat.getDict() for chat in chats]
            friends_data.append(friend_dict)


        return render(request, 'Friends.html', {
            'friends': friends_data
        })
    return redirect('/')
 
@login_required
def searchUser(request):
    if request.method == 'POST':
        targetUserName = ""
        targetSocialCode = ""
        bodyRequest = json.loads(request.body)
        print(bodyRequest)
        try:
            targetUserName = bodyRequest['username']
        except KeyError:
            pass
        try:
            targetSocialCode = bodyRequest['user_code']
        except KeyError:
            pass
        if targetUserName == "" and targetSocialCode == "":
            return JsonResponse({'error': 'Invalid request'}, status=400)
        targetUser = None
        if targetUserName != "":
            try:
                targetUser = MyUser.objects.get(username=targetUserName)
            except MyUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=400)

        if targetSocialCode != "":
            try:
                targetUser = MyUser.objects.get(userSocialCode=targetSocialCode)
            except MyUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=400)

        if targetUser:
            user_dict = targetUser.getDict()
            friend_request = FriendRequest.objects.filter(from_user=request.user, to_user=targetUser).first()
            user_dict['friend_request_status'] = friend_request.status if friend_request else None
            return JsonResponse({'user': user_dict})

        return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def Game(request):
    if(request.user.is_authenticated):
        return render(request, 'Game.html')
    return redirect('/')