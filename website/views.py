from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import signup_form


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    #why the empty {}?
    return render(request, './home.html', {})


def login_user(request):
    #checking and geting user data
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #authenticate user
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in")
            return redirect('home')
        else:
            messages.success(request,"Error logging in... check username and password")
            return redirect('login')
    else:
        return render(request, './login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You are logged out... ")
    return redirect('login')

def signup_user(request):
    if request.method == 'POST':
        form = signup_form(request.POST)
        
        if form.is_valid():
            form.save()
            
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "you signed up successfully")
            return redirect('home')
        
        else:
            messages.success(request, "Error signing up... ")
            return redirect('signup')
    else:
        form = signup_form()
        return render(request, './signup.html', {'form': form})