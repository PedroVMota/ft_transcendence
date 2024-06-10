#Auth/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.sessions.models import Session
from .serializers import UserSerializer, SessionSerializer
from rest_framework import status, permissions
from django.contrib.auth import login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.forms.models import model_to_dict
from django.core.files.storage import default_storage
import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.forms.models import model_to_dict
import json
from django.db.models.fields.files import ImageFieldFile


class utils:
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            return json.JSONEncoder.default(self, obj)



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






class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user_dict = model_to_dict(self.user)
        # Convert the image field to its URL
        user_dict['profile_picture'] = self.user.profile_picture.url
        data['user'] = user_dict  # Add user information to the response
        return data

class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            User = get_user_model()
            sessions = Session.objects.filter(expire_date__gte=timezone.now(), session_key=request.session.session_key)
            if not sessions.exists():
                request.session.create()
            response_data = serializer.validated_data
            response_data['sessionid'] = request.session.session_key  # Add session id to the response data
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie('sessionid', request.session.session_key, samesite='None', secure=True)
            return response
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
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

        