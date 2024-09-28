from django import forms
from django.contrib.auth.models import User
from .models import MyUser

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    profile_banner = forms.ImageField(required=False)

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'profile_picture', 'profile_banner']