#Auth/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.sessions.models import Session
from .serializers import UserSerializer, SessionSerializer
from rest_framework import status, permissions
import json




""" HOW TO USE THIS API

    Register a user is just a simple post request to the /register/ endpoint
    The body should be something like: /token/register
    
    {
        "username": "johndoe",
        "password": "securepassword",
        "email": "johndoe@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    Login is done by sending a post request to the /login/ endpoint with the body: /token
    {
        "username": "johndoe",
        "password": "securepassword"
    }
    
    The response will contain the access token and refresh token, which should be stored by the client.
    
    
    to update the acess token, send a post request to the /refresh/ endpoint with the body: /token/refresh
        
    {
        "refresh": "refresh_token"
    }


"""

class UserRegistrationView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class closeSession(APIView):
    """
    Using the acess token this view should close the session
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        try:
            request.session.flush()
            return Response({"message":"Session Closed"}, status=200)
        except Exception as e:
            return Response({"message":str(e)}, status=400)
        
        
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)



class HomeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)