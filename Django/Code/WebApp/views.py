from django.shortcuts import render
from django.http import JsonResponse







def index(request):
    return render(request, 'register.html')

def home(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def Profile(request):
    return render(request, {'foo': 'bar'}) # This is a placeholder for now

def logout(request):
    return render(request, 'logout.html')

def profile(request):
    return JSONResponse({'foo': 'bar'}) # This is a placeholder for now
