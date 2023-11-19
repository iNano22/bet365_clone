from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login_view', views.login_view, name="login_view"),
    path('registration', views.registration, name="registration"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('match_odds/<int:match_id>/', views.match_odds, name='match_odds'),
]
