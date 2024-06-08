#Auth/serializers.py
from rest_framework import serializers
from Auth.models import MyUser
from django.contrib.sessions.models import Session

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'profile_picture')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = MyUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Session
        fields = '__all__'
        
    def get_field_info(self, field_name):
        return self.fields[field_name]