from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime


def home(request):
    return render(request, 'bettingapp/index.html',{'teams':matches_data})


def login_view(request):
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
            login(request, user) 
            messages.success(request, "Logged in successfully")
            return render(request, "bettingapp/index.html", {"username": username,'data': 'dsadadss'})
        else:
            messages.error(request, "Bad credentials")
            return redirect('login_view')  
    return render(request, "bettingapp/index.html")


def index(request):
    return render(request, 'bettingapp/index.html', {
        'username': request.person.username,
        'messages': messages.get_messages(request),
    })


def signout(request):
    logout(request)
    messages.success(request, "Logged out in successfully")
    return redirect("home") 


import http.client
import json

def get_football_data(endpoint, headers):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    conn.request("GET", "/fixtures?live=all", headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    # Check if the response is in JSON format
    try:
        data = json.loads(data)
        team_info = data["response"]
    
    except json.JSONDecodeError:
        pass

    conn.close()
    return team_info

# Example usage to get matches
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "a10dd4036df5c7323538e962bbac57a6"
}

matches_endpoint = "/teams"
matches_data = get_football_data(matches_endpoint, headers)
