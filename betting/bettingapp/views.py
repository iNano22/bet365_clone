from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
import http.client
import json


def home(request):
    # Fetch data from the API every time the home page is loaded
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "a10dd4036df5c7323538e962bbac57a6"
    }

    fixtures = get_football_data("/fixtures?live=all", headers)
    odds=get_football_data("/odds/live", headers)
    getFixturesWithOdds(fixtures,odds)
    return render(request, 'bettingapp/index.html', {'fixtures': fixtures})


def getFixturesWithOdds(fixtures, odds):
    # Iterate through fixtures and add odds where fixture.id matches
    for index,fixture in enumerate(fixtures):
        for odd in odds:
            
            if fixture['fixture']['id'] == odd['fixture']['id']:
                   fixtures[index]['odds']=odd
            

    # Return the updated fixtures
    return fixtures

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
            return render(request, "bettingapp/index.html", {"username": username})
        else:
            messages.error(request, "Bad credentials")
            return redirect('login_view')  
    return render(request, "bettingapp/index.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out in successfully")
    return redirect("home") 




def get_football_data(endpoint, headers):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    conn.request("GET", endpoint, headers=headers)

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



