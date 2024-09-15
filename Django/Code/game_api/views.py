from django.shortcuts import render
from django.http import JsonResponse
from Auth.models import MyUser, GameRoom
from django.views.decorators.http import require_POST
import json


# Create your views here.
def generate(request):
    print(f"Type of request: {type(request)}")
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    if request.user.is_authenticated:
        user = request.user
        Name = request.POST.get('Name', "Game Room")
        room = GameRoom.objects.create(PlayerOne=user, GameName=Name)
        room.save()
        roomData = room.getDict()
        print(f"Room Data: {roomData}")
        return JsonResponse(roomData, status=201, safe=False)
    else:
        return JsonResponse({'error': "Forbidden"}, status=403)
    

def get(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    if request.user.is_authenticated:
        rooms = GameRoom.objects.filter(GameStates=2)
        roomData = [room.getDict() for room in rooms]
        print(f"Room Data: {roomData}")
        return JsonResponse(roomData, status=200, safe=False)
    else:
        return JsonResponse({'error': "Forbidden"}, status=403)
    
@require_POST
def join_game(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    
    user = request.user
    JsonData: dict = json.loads(request.body)
    RoomIdD = JsonData.get('RoomId', None)
    if not RoomIdD:
        return JsonResponse({'error': 'RoomId is required'}, status=400)
    try:
        room = GameRoom.objects.get(roomId=RoomIdD)
    except GameRoom.DoesNotExist:
        return JsonResponse({'error': 'Room does not exist'}, status=404)
    
    try:
        room.join_player(user)
    except ValueError as e:
        return JsonResponse({'error': "User is already a player"}, status=201)

    dictData = room.getDict()
    return JsonResponse(dictData, status=200, safe=False)

@require_POST
def leave_game(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    
    user = request.user
    JsonData: dict = json.loads(request.body)
    RoomIdD = JsonData.get('RoomId', None)
    if not RoomIdD:
        return JsonResponse({'error': 'RoomId is required'}, status=400)
    try:
        room = GameRoom.objects.get(roomId=RoomIdD)
    except GameRoom.DoesNotExist:
        return JsonResponse({'error': 'Room does not exist'}, status=404)
    
    try:
        room.leave_player(user)
    except ValueError as e:
        return JsonResponse({'error': "User is not a player"}, status=201)

    dictData = room.getDict()
    return JsonResponse(dictData, status=200, safe=False)