"""Core views: simple template renders for the marketing/public pages.

The `current_page` context value drives the "active" state (bold + always-on squiggle)
on the corresponding link in the header partial.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .forms import CustomUserCreationForm
import traceback

def home(request):
    return render(request, "core/home.html", {"current_page": "home"})


def about(request):
    return render(request, "core/about.html", {"current_page": "about"})


def faq(request):
    return render(request, "core/faq.html", {"current_page": "faq"})

def contact(request):
    return render(request, "core/contact.html", {"current_page": "contact"})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("core:home"))
        else:
            return render(request, "core/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("core:home"))

def redirect_by_role(user):
    if user.role == User.Role.TEACHER:
        return redirect('dashboard')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')  # <--- Catch selected role here
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')

        if password != confirmation:
            return render(request, 'core/register.html', {'message': 'Passwords do not match.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {'message': 'That username is already taken.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'core/register.html', {'message': 'An account with that email already exists.'})

        # Save user with role
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role  # <--- Pass the role into your User model
            )
        except IntegrityError:
            return render(request, 'core/register.html', {'message': 'That username or email is already taken.'})

        # Log in or redirect
        return redirect('core:login_view')

    return render(request, 'core/register.html')