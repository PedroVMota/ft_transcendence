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
from django.contrib.auth.decorators import login_required
from Lobby.models import Lobby
from django.http import HttpResponse
from Game.views import HTTP_CODES

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
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    data = json.loads(request.body)
    user_code = ""
    username = ""

    if 'user_code' in data:
        user_code = data.get('user_code')
    else:
        return JsonResponse({'error': 'Invalid request data'}, status=400)
    
    try:
        target_user = MyUser.objects.get(userSocialCode=user_code)
    except MyUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    from_user = request.user
    friend_request = FriendRequest.objects.create(from_user=from_user, to_user=target_user)
    notification = Notification.objects.create(user=target_user, message=f"{from_user.username} sent you a friend request.")

    friend_request.save()
    notification.save()
    # Send notification to target user
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
            'request_type': fr.type, #output can be friend_request or lobby_invite
            'requestUrl': fr.urlLobby if fr.urlLobby else None,
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
    print(json.dumps(data, indent=4))
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
        print("Sending friend request {}".format(request.body))
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


def accept_invite(request, fr: FriendRequest, noti: Notification):
    fr.status = 'accepted'
    fr.save()
    noti.save()
    print(f"Invite accepted: {fr.id}")
    return JsonResponse({
        'message': 'Invite accepted',
        'url': fr.urlLobby
        })

def reject_invite(fr: FriendRequest, noti: Notification):
    fr.status = 'rejected'
    fr.save()
    noti.save()
    print(f"Invite rejected: {fr.id}")
    return JsonResponse({'message': 'Invite rejected'})



@login_required
def manage_invite(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=200)
    data = json.loads(request.body)
    print(json.dumps(data, indent=4))
    invite_id = data.get('invite_id')
    action = data.get('action')
    try:
        print("'=========== Invite ID: ", invite_id)
        print("'=========== Invite Action: ", action)
        fr = FriendRequest.objects.get(id=invite_id, to_user=request.user)
    except FriendRequest.DoesNotExist:
        return JsonResponse({'error': 'Invite not found'}, status=200)
    
    try:
        invite = Notification.objects.get(fr=fr)
    except Notification.DoesNotExist:
        return JsonResponse({'error': 'Notification not found'}, status=200)

    if action == 'accept':
        return accept_invite(request, fr, invite)
    elif action == 'reject':
        return reject_invite(fr, invite)

    return JsonResponse({'error': 'Invalid action'}, status=400)




@login_required
def inviteToLobby(request: HttpResponse, lobbyId: str):
    if request.method != 'POST':
        print("Invalid request method")
        response = {'error': 'Invalid request method', 'Lobby': None}
        return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])
    if(not lobbyId):
        print("LobbyId is required to invite")
        response = {'error': 'LobbyId is required to invite', 'Lobby': None}
    lobby = None
    try:
        print("Finding lobby")
        lobby = Lobby.objects.get(id=lobbyId)
    except Lobby.DoesNotExist:
        print("Lobby not found")
        response = {'error': 'Lobby not found', 'Lobby': None}
        return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["NOT_FOUND"])
    
    print("Inviting user to lobby")
    json_body = json.loads(request.body)
    userCodeToInvite = json_body.get('to')
    print(f"User code to invite: {userCodeToInvite}")
    url= f"/Lobby/{lobbyId}"
    try:
        print("Creating notification")
        request: Notification = Notification.objects.create(user=request.user, type='lobby_invite', message=f"You have been invited to a lobby", url=url)
        request.save()
        print("Creating friend request")
        friendReq = FriendRequest.objects.create(from_user=request.user, to_user=MyUser.objects.get(userSocialCode=userCodeToInvite), urlLobby=url, type='lobby_invite', noti=request)
        friendReq.save()
        request.fr = friendReq
        request.save()
    except Exception as e:
        response = {'error': f"Error inviting user to lobby: {e}", 'Lobby': None}
        return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])
    channel = get_channel_layer()
    async_to_sync(channel.group_send)(
        f"user_{userCodeToInvite}",
        {
            'type': 'Notification',
            'notifications': f'{request.message}'
        }
    )
    response = {'message': 'User invited to lobby', 'Lobby': None}
    return JsonResponse(response, status=HTTP_CODES["SUCCESS"]["CREATED"])
    