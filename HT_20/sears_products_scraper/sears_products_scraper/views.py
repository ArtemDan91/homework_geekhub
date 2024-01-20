from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"{user}, you have successfully logged in!")
            return redirect('index')
        else:
            messages.error(request, 'Login failed. The provided username or password is incorrect or the user is not registered!')
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, f"You have successfully logged out!")
    return redirect('login')