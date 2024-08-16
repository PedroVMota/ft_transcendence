from django.shortcuts import render
from django.http import JsonResponse









def index(request):
    if(request.user.is_authenticated):
        return render(request, 'index.html', {'user': request.user})
    else:
        return render(request, 'register.html')

def home(request):
    if(request.user.is_authenticated):
        return render(request, 'index.html')
    else:
        return render(request, 'register.html')

def Auth(request):
    if(request.user.is_authenticated):
        return render(request, 'profile.html')
    else:
        return render(request, 'register.html')

def Profile(request):
    if(request.user.is_authenticated):
        return render(request, 'profile.html')
    else:
        return render(request, 'register.html')

def logout(request):
    if(request.user.is_authenticated):
        return render(request, 'profile.html')
    else:    
        return render(request, 'register.html')

def profile(request):
    if(request.user.is_authenticated):
        return render(request, 'profile.html')
    else:
        return render(request, 'register.html')
