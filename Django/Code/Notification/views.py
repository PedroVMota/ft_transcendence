from django.shortcuts import render
from django.http import JsonResponse
import Auth.models as MyUser
import json
from .models import FriendRequest, Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.response import Response
from Auth.models import MyUser

# FRIEND REQUEST HANDLING
# UTILS

def accept_friend_request(request, friend_request):
    friend_request.status = 'accepted'
    friend_request.save()

    User: MyUser = request.user
    User.__add__user__(friend_request.from_user)

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
    target_user = MyUser.objects.get(userSocialCode=TargetUserCode)
    print(" _________ ", target_user)
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




# NOTIFICATIONS
def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications_data = [{'message': notification.message} for notification in notifications]
        return JsonResponse({'notifications': notifications_data})
    else:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)




# FRIEND REQUEST HANDLING
