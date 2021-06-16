from django.shortcuts import render
from django.contrib.auth import logout
from substitution.constants import LOG_OUT_OK

from .services import signup_service, signin_service


# Create your views here.

def signup(request):
    """view when a user register to the website"""
    context = signup_service(request)
    return render(request, 'signin.html', context)


def signin(request):
    """view managing user log-in to the website"""
    html_page = signin_service(request)[0]
    context = signin_service(request)[1]
    return render(request, html_page, context)


def logout_user(request):
    """view managing user log-out"""
    logout(request)
    user_message = LOG_OUT_OK
    return render(request, 'home.html', {'user_message': user_message})


def user(request):
    """view managing the acess to the user's saveds alternatives page"""
    return render(request, 'user.html')
