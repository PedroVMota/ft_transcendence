from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from Auth.models import MyUser
from .models import Game, Tournament
import json


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


def CreateIndividualGame(request: HttpResponse):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=HTTP_CODES["CLIENT_ERROR"]["METHOD_NOT_ALLOWED"])
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=HTTP_CODES["CLIENT_ERROR"]["UNAUTHORIZED"])
    
    try:
        data = json.loads(request.body)
        try:
            newGame: Game = Game.objects.create(pOne=request.user)
            newGame.save()
            return JsonResponse({"game": newGame.getDict()}, status=HTTP_CODES["SUCCESS"]["CREATED"])
        except:
            return JsonResponse({"error": "Error creating game"}, status=HTTP_CODES["SERVER_ERROR"]["INTERNAL_SERVER_ERROR"])


    except:
        return JsonResponse({"error": "Invalid JSON"}, status=HTTP_CODES["CLIENT_ERROR"]["BAD_REQUEST"])



def locaIndex(request):
    print(request.method)
    if request.method != "GET":
        return JsonResponse({"error": "Invalid method"}, status=HTTP_CODES["CLIENT_ERROR"]["METHOD_NOT_ALLOWED"])
    # send the index.html
    allGames = Game.objects.all()
    allTournaments = Tournament.objects.all()
    Objects = {
        "Games": [ game.getDict() for game in allGames ],
        "Tournaments": [ tournament.getDict() for tournament in allTournaments ]
    }
    print(Objects)
    return render(request, "GameMonitor.html", Objects)