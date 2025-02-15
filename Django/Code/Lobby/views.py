
from Lobby.models import Lobby as LobbyModel
from Game.views import HTTP_CODES # todo -> put this somewhere else, that is make HTTP_CODES somewhat a global stuff

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import json
import random

@login_required
def getLobbyInformation(request: HttpResponse):
    if request.method == 'POST':
        user = request.user
        user_lobbies = LobbyModel.objects.filter(players=user)

        if user_lobbies.exists():
            user_lobby = user_lobbies.first()
            response = {
                'error': 'You are already in a lobby',
                'Lobby': user_lobby.getDict()
            }
            return JsonResponse(response, status=HTTP_CODES["SUCCESS"]["OK"])

        try:
            body = json.loads(request.body)
            LobbyName = body.get('LobbyName', '')
        except json.JSONDecodeError:
            LobbyName = ''

        if not LobbyName:
            response = {'error': 'LobbyName is required', 'Lobby': None}
            return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])

        try:
            lobbyInstance = LobbyModel.objects.get(name=LobbyName)
        except LobbyModel.DoesNotExist:
            print("All Lobbies: ", LobbyModel.objects.all())
            response = {'error': 'Lobby not found', 'Lobby': None}
            return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["NOT_FOUND"])

        response = {'Lobby': lobbyInstance.getDict()}
        return JsonResponse(response, status=HTTP_CODES["SUCCESS"]["OK"])

    response = {'error': 'Invalid request method', 'Lobby': None}
    return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])


@login_required
def createLobby(request: HttpRequest):
    if request.method == 'POST':
        user = request.user
        user_lobbies = LobbyModel.objects.filter(players=user)
        if user_lobbies.exists():
            user_lobby = user_lobbies.first()
            response = {
                'error': 'You are already in a lobby',
                'Lobby': user_lobby.getDict()
            }
            print("Response Body:", response)
            return JsonResponse(response, status=HTTP_CODES["SUCCESS"]["OK"])

        try:
            body = json.loads(request.body)
            print("Request Body:", body)
        except json.JSONDecodeError:
            response = {'error': 'Invalid JSON', 'Lobby': None}
            print("Response Body:", response)
            return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])

        lobby_name = body.get('LobbyName')
        if not lobby_name:
            response = {'error': 'LobbyName is required', 'Lobby': None}
            print("Response Body:", response)
            return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])

        if LobbyModel.objects.filter(name=lobby_name).exists():
            lobby_data = LobbyModel.objects.get(name=lobby_name)
            try:
                lobby_data.joinPlayer(user)
                response = {
                    'message': 'User added to lobby',
                    'Lobby': lobby_data.getDict()
                }
                return JsonResponse(response, status=HTTP_CODES["SUCCESS"]["OK"])
            except:
                pass
        lobby = LobbyModel(name=lobby_name)
        print("saving lobby with Id: ", lobby.id)
        lobby.save()
        try:
            lobby.joinPlayer(user)  # Add the user to the players list
            response = {
                'message': 'Lobby created and user added',
                'Lobby': lobby.getDict()
            }
            return JsonResponse(response, status=HTTP_CODES["SUCCESS"]["CREATED"])
        except:
            pass
        response = {'error': 'Failed to add user to lobby', 'Lobby': None}
        print("Response Body:", response)
        return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])

    response = {'error': 'Invalid request method', 'Lobby': None}
    print("Response Body:", response)
    return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])


@login_required
def MyLobby(request, lobby_id=None):
    if request.method == 'GET':
        if request.user.is_authenticated:
            p_one = None
            p_two = None
            lobby = None
            try:
                lobby = LobbyModel.objects.get(id=lobby_id)
                print(f"Lobbies: {str(lobby.id)}")
                players = lobby.players.all()
                if lobby.isFull() and not (players.filter(id=request.user.id)).exists():
                    return redirect("/")
                if not (players.filter(id=request.user.id)).exists():
                    lobby.joinPlayer(request.user)
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f"lobby_{lobby_id}",{
                            'type': 'refresh',
                        }
                    )
                players = lobby.players.all()
                if len(players) == 1:
                    p_one = players[0].getDict()
                if len(players) == 2:
                    p_one = players[0].getDict()
                    p_two = players[1].getDict()
            except LobbyModel.DoesNotExist:
                print("Lobby not found", lobby_id)
                return redirect("/")
            
            random_color_hex = f"#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            random_ball_color = f"#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            data = {
                'lobby': lobby,
                'first_player': p_one,
                'second_player': p_two,
                'random_color_hex': random_color_hex,
                'random_ball_color': random_ball_color
            }
           
            return render(request, 'Lobby.html', data)

    else:
        response = {
            'error': 'Invalid request method',
            'Lobby': None
        }
        return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])
