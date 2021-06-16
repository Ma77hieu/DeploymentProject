from django.shortcuts import render
from authentification.forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from substitution.constants import LOG_IN_OK, INVALID_CREDENTIALS


# Create your views here.

def login_user(request, user_name, pwd, signup):
    """function used to authenticate a user.
    This function is called when user signin and/or signup"""
    auth = authenticate(request, username=user_name,
                        password=pwd)
    if auth is not None:
        logged_user = login(request, auth)
        if signup is True:
            html_page = 'signin.html'
        else:
            html_page = 'user.html'
        return render(request, html_page, {
            'form': logged_user})
    else:
        return INVALID_CREDENTIALS


def signup_service(request):
    """function called when a user register to the website"""
    if request.method == "GET":
        form = UserForm()
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form_update = form.save(commit=False)
            form_update.password = make_password(form.cleaned_data['password'])
            form_update.save()
            user_name = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            signup = True
            login_user(request, user_name, pwd, signup)

        else:
            messages.error(
                request, "Unsuccessful registration. Invalid information.")
            signup = False

    return ({'form': form, 'signup': signup})


def signin_service(request):
    """function called when a user log-in to the website"""
    if request.method == "GET":
        form = UserForm()
        return ('signin.html', {'form': form})
    elif request.method == "POST":
        user_name = request.POST['username']
        pwd = request.POST['password']
        signup = False
        login = login_user(request, user_name, pwd, signup)
        if login == INVALID_CREDENTIALS:
            form = UserForm()
            return ('signin.html',
                    {'form': form, 'error': INVALID_CREDENTIALS})
        else:
            return ('user.html', {'user_message': LOG_IN_OK})
