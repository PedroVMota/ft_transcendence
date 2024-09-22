from django.contrib.auth import login
from rest_framework import status
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
from django.utils.decorators import method_decorator
import json
from Auth.models import MyUser, currentChat, FriendRequest, Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404





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

@csrf_exempt
def user_data(request):
    if request.user.is_authenticated:
        user: MyUser = request.user
        return JsonResponse(user.getJson(), status=200)
    else:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
def update_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)

    try:
        user = request.user
        data = json.loads(request.body)
    except (json.JSONDecodeError, AttributeError) as e:
        return JsonResponse({'error': 'Invalid data format.'}, status=400)

    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.about_me = data.get('about_me', user.about_me)

    profile_picture = request.FILES.get('profile_picture')
    if profile_picture:
        valid_extensions = ['png', 'webp', 'gif', 'jpg', 'jpeg']
        extension = profile_picture.name.split('.')[-1].lower()
        if extension not in valid_extensions:
            return JsonResponse({'error': f'Unsupported file extension. Allowed extensions are: {", ".join(valid_extensions)}'}, status=400)
        user.profile_picture = profile_picture

    try:
        user.save()
    except Exception as e:
        return JsonResponse({'error': 'Failed to update profile.'}, status=500)

    return JsonResponse({'message': 'Profile updated successfully!'})



@csrf_exempt
def FriendChat(request):
    if request.user.is_authenticated:
        currentChats = currentChat.objects.filter(members=request.user)
        chat_data = []
        for chat in currentChats:
            for member in chat.members.exclude(id=request.user.id):
                chat_data.append({
                    'username': member.username,
                    'email': member.email,
                    'profile_picture': member.profile_picture.url,
                    'unique_id': chat.unique_id,
                    'targetUserUUID': member.userSocialCode
                })
        return JsonResponse({'chats': chat_data})
    else:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
def block_list(request):
    if request.user.is_authenticated:
        user: MyUser = request.user
        return JsonResponse(user.getBlockedUsers(), status=200)
    else:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
@csrf_exempt
def block_user(request, socialCode):
    if request.user.is_authenticated:
        user: MyUser = request.user
        try:
            friend = MyUser.objects.get(userSocialCode=socialCode)
            user.blockUser(friend)
            return Response({'message': 'User blocked'}, status=200)
        except MyUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    else:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
def remove(request, socialCode):
    if request.user.is_authenticated:
        user: MyUser = request.user
        try:
            friend = MyUser.objects.get(userSocialCode=socialCode)
            user.removeFriend(friend)
            return Response({'message': 'Friend removed'}, status=200)
        except MyUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    else:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)












# NOTIFICATIONS
@csrf_exempt
def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications_data = [{'message': notification.message} for notification in notifications]
        return JsonResponse({'notifications': notifications_data})
    else:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

















# FRIEND REQUEST HANDLING
# UTILS

def accept_friend_request(request, friend_request):
    friend_request.status = 'accepted'
    friend_request.save()
    request.user.friendlist.add(friend_request.from_user)
    friend_request.from_user.friendlist.add(request.user)
    request.user.save()
    friend_request.from_user.save()

    conversation = currentChat.objects.create()
    conversation.members.add(request.user, friend_request.from_user)
    conversation.save()


    print(f"Friend request accepted: {friend_request.id}")
    return JsonResponse({'message': 'Friend request accepted'})

def reject_friend_request(friend_request):
    friend_request.status = 'rejected'
    friend_request.save()
    print(f"Friend request rejected: {friend_request.id}")
    return JsonResponse({'message': 'Friend request rejected'})


def handle_friend_request(request):
    TargetUserCode = json.loads(request.body)['user_code']
    if TargetUserCode == request.user.userSocialCode:
        return JsonResponse({'error': 'You cannot send a friend request to yourself'}, status=400)
    try:
        target_user = MyUser.objects.get(userSocialCode=TargetUserCode)
    except MyUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    from_user = request.user
    if FriendRequest.objects.filter(from_user=from_user, to_user=target_user, status='pending').exists():
        return JsonResponse({'error': 'Friend request already sent'}, status=400)
    friend_request = FriendRequest.objects.create(from_user=from_user, to_user=target_user)
    notification = Notification.objects.create(user=target_user, message=f"{from_user.username} sent you a friend request.")

    friend_request.save()
    notification.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{target_user.userSocialCode}",
        {
            'type': 'Notification',
            'notifications': f'{notification.message}'
        }
    )
    return JsonResponse({'message': 'Friend request sent successfully!'})





# GETTER
def get_request(request):
    if request.user.is_authenticated:
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
        requests_data = [{
            'request_id': fr.id,
            'from_user': fr.from_user.username,
            'from_user_id': fr.from_user.id,
            'from_user_profile_picture': fr.from_user.profile_picture.url
        } for fr in pending_requests]
        
        print(requests_data)
        return JsonResponse({'friend_requests': requests_data})
    else:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
# MANAGE
def manage_request(request):
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

# SEND


def send_request(request):
    if request.method == 'POST':
        return handle_friend_request(request)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



# FRIEND REQUEST HANDLING
