from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from Auth.models import MyUser
from Lobby.models import Lobby as LobbyModel
from .models import Game

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
def getGame(request):
	if request.method == 'POST':
		print("creating game")

		body = json.loads(request.body)
		user = request.user.getDict()
		lobby = LobbyModel.objects.get(id=body['uuid'])
		if len(lobby.players.all()) == 2:
			lobby_dict = lobby.getDict()
			player_one_user_code = lobby_dict['Players'][0]["Info"]["userCode"]
			player_two_user_code = lobby_dict['Players'][1]["Info"]["userCode"]
			user_code = user["Info"]["userCode"]

			print("requesting user:", user_code, "player1:", player_one_user_code, "player2:", player_two_user_code)

			if user_code == player_one_user_code or user_code == player_two_user_code:
				game_id = lobby_dict['Game']['uuid']

				response = {
					'gameId': game_id,
				}
				return JsonResponse(response, status=HTTP_CODES["SUCCESS"]["CREATED"])
			else:
				response = {
					'error': 'player must be in the lobby',
					'Lobby': None,

				}
				return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])
		else:
			response = {'error': 'Lobby must have two players', 'Lobby': None}
			return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])

	response = {
		'error': 'Invalid request method',
		'Lobby': None
	}
	return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])

@login_required
def MyGame(request, game_id=None):
	if request.method == 'GET':
		print("get/game request is: ", request)
		user = request.user.getDict()
		lobby = LobbyModel.objects.filter(game=game_id).get()
		print("received game id ", game_id)
		print("lobby game id", lobby.game.id)
		if str(lobby.game.id) == str(game_id):
			lobby_dict = lobby.getDict()
			player_one_user_code = lobby_dict['Players'][0]["Info"]["userCode"]
			player_two_user_code = lobby_dict['Players'][1]["Info"]["userCode"]
			user_code = user["Info"]["userCode"]

			if user_code == player_one_user_code or user_code == player_two_user_code:
				return render(request, 'Game.html',{
					'game_id': game_id
			})
			else:
				print("redirecting to: /")
				return redirect("/")
		else:
			print("redirecting")
			return redirect("/")
	else:
		response = {
			'error': 'Invalid request method',
			'Lobby': None
		}
		return JsonResponse(response, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])


@login_required
def leave_lobby(request):
    print("[LEAVE LOBBY] User")
    user = request.user  # Ensure the user is obtained from the request
    print(f"[LEAVE LOBBY] User: {user.id}")
    try:
        print("[LEAVE LOBBY] Try")
        lobby = LobbyModel.objects.get(players=user)
        print("[LEAVE LOBBY] Lobby")
        lobby.disconnectPlayer(user)
        print("[LEAVE LOBBY] Disconnect")
        return JsonResponse({'message': 'Player left lobby'}, status=HTTP_CODES["SUCCESS"]["OK"])
    except LobbyModel.DoesNotExist:
        print("[LEAVE LOBBY] Lobby not found")
        return JsonResponse({'error': 'Lobby not found'}, status=HTTP_CODES["CLIENT_ERROR"]["NOT_FOUND"])
    except Exception as e:
        print(f"[LEAVE LOBBY] Failed to leave lobby: {str(e)}")
        return JsonResponse({'error': 'Failed to leave lobby'}, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])
