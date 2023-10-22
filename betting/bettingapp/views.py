from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'bettingapp/index.html')


def login(request):
    return render(request, 'bettingapp/login.html')


def registration(request):
    return render(request, 'bettingapp/registration.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['re_password']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('registration')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('registration')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters!")
            return redirect('registration')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('registration')

        if password != re_password:
            messages.error(request, "Password didn't match!")
            return redirect('registration')

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()
    return render(request, 'bettingapp/index.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request)  # Make sure to include 'user' here
            messages.success(request, "Logged in successfully")
            return render(request, "bettingapp/index.html", {"username": username})
        else:
            messages.error(request, "Bad credentials")
            return redirect('login')
    return render(request, "bettingapp/index.html")


def index(request):
    return render(request, 'bettingapp/index.html',
                  {'username': request.person.username, 'messages': messages.get_messages(request)})


def signout(request):
    logout(request)
    messages.success(request, "Logged out in successfully")
    return render(request, "bettingapp/index.html")