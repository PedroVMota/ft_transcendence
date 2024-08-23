from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm, ProfileForm
from django.contrib.auth import authenticate, login, logout as auth_logout



def Menu(request):
    return render(request, 'Components/Menu.html')

@login_required
def index(request):
    return render(request, 'index.html', {'user': request.user})


from django.shortcuts import render
from .forms import LoginForm, RegistrationForm

def login_register_view(request):
    print(request.method)
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'message': 'Login successful'})
                else:
                    return JsonResponse({'error': 'Invalid username or password'}, status=400)
            return JsonResponse({'error': 'Invalid form data'}, status=400)
        elif 'register' in request.POST:
            register_form = RegistrationForm(request.POST)
            if register_form.is_valid():
                if register_form.cleaned_data['password'] != register_form.cleaned_data['password_confirm']:
                    return JsonResponse({'error': 'Passwords do not match'}, status=400)
                user = register_form.save(commit=False)
                user.save()
                return JsonResponse({'message': 'Registration successful'})
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        login_form = LoginForm()
        register_form = RegistrationForm()
    return render(request, 'register.html', {'login_form': login_form, 'register_form': register_form})


def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({'message': 'Logout successful'})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Profile')  # Redirect to a profile page or any other page
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'Profile.html', {'form': form, 'user': request.user})
    
def Friends(request):
    if(request.user.is_authenticated):
        return render(request, 'Friends.html')
    return redirect('/')
