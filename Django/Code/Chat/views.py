from rest_framework.response import Response
from django.http import JsonResponse
from Chat.models import currentChat
from rest_framework import status
import json

def FriendChat(request):
    if request.user.is_authenticated:
        currentChats = currentChat.objects.filter(members=request.user)
        # currentChats = request.user.getChatData()
        chat_data = []
        for chat in currentChats:
            for member in chat.members.exclude(id=request.user.id):
                chat_data.append({
                    'first_name': member.first_name,
                    'email': member.email,
                    'profile_picture': member.profile_picture.url,
                    'unique_id': chat.unique_id.hex,
                    'targetUserUUID': member.userSocialCode
                })
        # print a pretty json with chat_data
        print(f">>", json.dumps(chat_data, indent=4))
        return JsonResponse({'chats': chat_data})
    else:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)