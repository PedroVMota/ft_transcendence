from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from norminette.rules.check_operators_spacing import lnests

from Auth.models import MyUser
from .models import Game, Lobby

#from Game.Game import activeGames

import json
from django.contrib.auth.decorators import login_required


HTTP_CODES = {
    # Informational responses (100–199)
    "INFORMATIONAL": {
        "CONTINUE": 100,
        "SWITCHING_PROTOCOLS": 101,
        "PROCESSING": 102,
        "EARLY_HINTS": 103,
    },
    
    # Successful responses (200–299)
    "SUCCESS": {
        "OK": 200,
        "CREATED": 201,
        "ACCEPTED": 202,
        "NON_AUTHORITATIVE_INFORMATION": 203,
        "NO_CONTENT": 204,
        "RESET_CONTENT": 205,
        "PARTIAL_CONTENT": 206,
        "MULTI_STATUS": 207,
        "ALREADY_REPORTED": 208,
        "IM_USED": 226,
    },
    
    # Redirection messages (300–399)
    "REDIRECTION": {
        "MULTIPLE_CHOICES": 300,
        "MOVED_PERMANENTLY": 301,
        "FOUND": 302,
        "SEE_OTHER": 303,
        "NOT_MODIFIED": 304,
        "USE_PROXY": 305,
        "TEMPORARY_REDIRECT": 307,
        "PERMANENT_REDIRECT": 308,
    },
    
    # Client error responses (400–499)
    "CLIENT_ERROR": {
        "BAD_REQUEST": 400,
        "UNAUTHORIZED": 401,
        "PAYMENT_REQUIRED": 402,
        "FORBIDDEN": 403,
        "NOT_FOUND": 404,
        "METHOD_NOT_ALLOWED": 405,
        "NOT_ACCEPTABLE": 406,
        "PROXY_AUTHENTICATION_REQUIRED": 407,
        "REQUEST_TIMEOUT": 408,
        "CONFLICT": 409,
        "GONE": 410,
        "LENGTH_REQUIRED": 411,
        "PRECONDITION_FAILED": 412,
        "PAYLOAD_TOO_LARGE": 413,
        "URI_TOO_LONG": 414,
        "UNSUPPORTED_MEDIA_TYPE": 415,
        "RANGE_NOT_SATISFIABLE": 416,
        "EXPECTATION_FAILED": 417,
        "I_AM_A_TEAPOT": 418,  # Fun Easter egg response
        "MISDIRECTED_REQUEST": 421,
        "UNPROCESSABLE_ENTITY": 422,
        "LOCKED": 423,
        "FAILED_DEPENDENCY": 424,
        "TOO_EARLY": 425,
        "UPGRADE_REQUIRED": 426,
        "PRECONDITION_REQUIRED": 428,
        "TOO_MANY_REQUESTS": 429,
        "REQUEST_HEADER_FIELDS_TOO_LARGE": 431,
        "UNAVAILABLE_FOR_LEGAL_REASONS": 451,
    },
    
    # Server error responses (500–599)
    "SERVER_ERROR": {
        "INTERNAL_SERVER_ERROR": 500,
        "NOT_IMPLEMENTED": 501,
        "BAD_GATEWAY": 502,
        "SERVICE_UNAVAILABLE": 503,
        "GATEWAY_TIMEOUT": 504,
        "HTTP_VERSION_NOT_SUPPORTED": 505,
        "VARIANT_ALSO_NEGOTIATES": 506,
        "INSUFFICIENT_STORAGE": 507,
        "LOOP_DETECTED": 508,
        "NOT_EXTENDED": 510,
        "NETWORK_AUTHENTICATION_REQUIRED": 511,
    }
}


@login_required
def getLobbyInformation(request: HttpResponse):
    if request.method == 'POST':
        user = request.user
        user_lobbies = Lobby.objects.filter(players=user)
        
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
            lobbyInstance = Lobby.objects.get(name=LobbyName)
        except Lobby.DoesNotExist:
            print("All Lobbies: ", Lobby.objects.all())
            response = {'error': 'Lobby not found', 'Lobby': None}
            return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["NOT_FOUND"])
        
        response = {'Lobby': lobbyInstance.getDict()}
        return JsonResponse(response, status=HTTP_CODES["SUCCESS"]["OK"])
    
    response = {'error': 'Invalid request method', 'Lobby': None}
    return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])


@login_required
def createLobby(request: HttpResponse):
    if request.method == 'POST':
        user = request.user
        user_lobbies = Lobby.objects.filter(players=user)
        
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
        
        lobbyName = body.get('LobbyName')
        if not lobbyName:
            response = {'error': 'LobbyName is required', 'Lobby': None}
            print("Response Body:", response)
            return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])
        
        lobby = Lobby(name=lobbyName)
        print("saving lobby with Id: ", lobby.id)
        lobby.save()
        lobby.joinPlayer(user)  # Add the user to the players list
        response = {
            'message': 'Lobby created and user added',
            'Lobby': lobby.getDict()
        }
        print("Response Body:", response)
        return JsonResponse(response, status=HTTP_CODES["SUCCESS"]["CREATED"])
    
    response = {'error': 'Invalid request method', 'Lobby': None}
    print("Response Body:", response)
    return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])

@login_required
def getGame(request):
    if request.method == 'POST':
        print("creating game")

        body = json.loads(request.body)
        print("Request Body:", body)

        lobby = Lobby.objects.get(id=body['uuid'])
        if len(lobby.players.all()) == 2:
            lobby_dict = lobby.getDict()
            game_id = lobby_dict['Game']['uuid']
            print("gameId is: ", game_id)

            response = {
                'gameId': game_id,
            }

            return JsonResponse(response, status=HTTP_CODES["SUCCESS"]["CREATED"])
        else:
            response = {'error': 'Lobby must have two players', 'Lobby': None}
            return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])

    response = {
        'error': 'Invalid request method',
        'Lobby': None
    }
    return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])


@login_required
def MyLobby(request, lobby_id=None):
    if request.method == 'GET':
        print(" ==== GET LOBBY ==== ")
        if request.user.is_authenticated:
            pOne = None
            pTwo = None
            lobby = None
            try:
                lobby = Lobby.objects.get(id=lobby_id)

                players = lobby.players.all()

                # check if the user is already in the lobby
                if not (players.filter(id=request.user.id)).exists():
                    lobby.joinPlayer(request.user)

                players = lobby.players.all()

                if len(players) == 1:
                    pOne = players[0].getDict()
                if len(players) == 2:
                    pOne = players[0].getDict()
                    pTwo = players[1].getDict()

            except Lobby.DoesNotExist:
                print("Lobby not found", lobby_id)
                return redirect("/")

            data = {
                'lobby': lobby,
                'first_player': pOne,
                'second_player': pTwo
            }
            print("rendering Lobby.html with following data: ", data)
            return render(request, 'Lobby.html', data)

    else:
        response = {
            'error': 'Invalid request method',
            'Lobby': None
        }
        return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])

@login_required
def MyGame(request, game_id=None):
    if request.method == 'GET':
        print("get/game request is: ", request)

    return render(request, 'Game.html',
                  {
                      'game_id': game_id
                  })