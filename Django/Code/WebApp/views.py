from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout as auth_logout
from .forms import LoginForm, RegistrationForm, ProfileForm
from Auth.models import MyUser, Notification, FriendRequest
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import time
import os

def Menu(request):
    start_time = time.time()
    response = render(request, 'Components/Menu.html')
    end_time = time.time()
    print(f"\n\n\n\n\nMenu view processing time: {end_time - start_time} seconds")
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
        user.save()
        return JsonResponse({'message': 'Registration successful'})
    return JsonResponse({'error': 'Invalid form data'}, status=400)

@login_required
def getUserData(request):
    if request.method == 'GET':
        os.system('clear')
        print(request.user.getJson())
        return JsonResponse({'user': request.user.getJson()})

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({'message': 'Logout successful'})

@login_required
def edit_profile(request):
    if request.method == 'GET':
        return render(request, 'Profile.html')
    if request.method == 'POST':
        return handle_profile_update(request)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def handle_profile_update(request):
    if 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        print(f"File name: {uploaded_file.name}")
        print(f"File size: {uploaded_file.size} bytes")
        print(f"Content type: {uploaded_file.content_type}")
    else:
        print("No file found in the request.")
    
    user = request.user
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.about_me = request.POST.get('about_me')

    profile_picture = request.FILES.get('profile_picture')
    if profile_picture:
        valid_extensions = ['png', 'webp', 'gif']
        extension = profile_picture.name.split('.')[-1].lower()
        if extension not in valid_extensions:
            return JsonResponse({'error': f'Unsupported file extension. Allowed extensions are: {", ".join(valid_extensions)}'}, status=400)
        user.profile_picture = profile_picture
    
    user.save()
    return JsonResponse({'message': 'Profile updated successfully!'})

@login_required
def Friends(request):
    if request.user.is_authenticated:
        return render(request, 'Friends.html')
    return redirect('/')

def searchUser(request):
    if request.method == 'GET':
        friends = MyUser.objects.filter(userSocialCode=request.GET.get('user_code'))
        friends_data = [friend.getJson() for friend in friends]
        return JsonResponse({'friends': friends_data})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def send_friend_request(request):
    if request.method == 'POST':
        return handle_friend_request(request)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def handle_friend_request(request):
    TargetUserCode = json.loads(request.body)['user_code']
    try:
        target_user = MyUser.objects.get(userSocialCode=TargetUserCode)
    except MyUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    from_user = request.user
    if FriendRequest.objects.filter(from_user=from_user, to_user=target_user, status='pending').exists():
        return JsonResponse({'error': 'Friend request already sent'}, status=400)

    friend_request = FriendRequest.objects.create(from_user=from_user, to_user=target_user)
    notification = Notification.objects.create(user=target_user, message=f"{from_user.username} sent you a friend request.")

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{target_user.userSocialCode}",
        {
            'type': 'send_notification',
            'notifications': [{'message': notification.message}]
        }
    )

    return JsonResponse({'message': 'Friend request sent successfully!'})

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    notifications_data = [{'message': notification.message} for notification in notifications]
    return JsonResponse({'notifications': notifications_data})

@login_required
def get_friend_requests(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    requests_data = [{
        'request_id': fr.id,
        'from_user': fr.from_user.username,
        'from_user_profile_picture': fr.from_user.profile_picture.url,
        'created_at': fr.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for fr in pending_requests]
    return JsonResponse({'friend_requests': requests_data})

@login_required
def manage_friend_request(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    data = json.loads(request.body)
    friend_request_id = data.get('friend_request_id')
    action = data.get('action')
    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user)
    except FriendRequest.DoesNotExist:
        return JsonResponse({'error': 'Friend request not found'}, status=404)
    if action == 'accept':
        return accept_friend_request(request, friend_request)
    elif action == 'reject':
        return reject_friend_request(friend_request)
    return JsonResponse({'error': 'Invalid action'}, status=400)

def accept_friend_request(request, friend_request):
    friend_request.status = 'accepted'
    friend_request.save()
    request.user.friendlist.add(friend_request.from_user)
    friend_request.from_user.friendlist.add(request.user)
    request.user.save()
    friend_request.from_user.save()
    return JsonResponse({'message': 'Friend request accepted'})



""" 
    This function is used to reject a friend request.
    It sets the status of the friend request to 'rejected' and saves the changes to the database.
    :param friend_request: The friend request object to be rejected.
    :return: JsonResponse with a message indicating that the friend request has been rejected.
"""
def reject_friend_request(friend_request):
    friend_request.status = 'rejected'
    friend_request.save()
    return JsonResponse({'message': 'Friend request rejected'})