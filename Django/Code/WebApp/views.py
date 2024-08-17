from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest

def Menu(request):
    return render(request, 'Components/Menu.html')

def index(request):
    if(request.user.is_authenticated):
        return render(request, 'index.html', {'user': request.user})
    else:
        return render(request, 'register.html')

def Auth(request):
    return render(request, 'register.html')

def logout(request):
    return redirect('/')

def profile(request):
    if(request.user.is_authenticated):
        return render(request, 'Profile.html', {'user': request.user})
    else:
        return render(request, 'register.html')
    
def Friends(request):
    return render(request, 'Friends.html')
