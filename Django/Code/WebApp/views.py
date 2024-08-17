from django.shortcuts import render
from django.http import JsonResponse, HttpRequest






def Menu(request):
    return render(request, 'Components/Menu.html')

def index(request):
    if(request.user.is_authenticated):
        return render(request, 'index.html', {'user': request.user})
    else:
        return render(request, 'register.html')

def home(request):
    if(request.user.is_authenticated):
        return render(request, 'index.html', {'user': request.user})
    else:
        return render(request, 'register.html')

def Auth(request):
    return render(request, 'register.html')


def logout(request):
    return render(request, {'user': request.user})

def profile(request):
    if(request.user.is_authenticated):
        return render(request, 'profile.html', {'user': request.user})
    else:
        return render(request, 'register.html')
