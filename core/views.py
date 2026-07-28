"""Core views: simple template renders for the marketing/public pages.

The `current_page` context value drives the "active" state (bold + always-on squiggle)
on the corresponding link in the header partial.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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

def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "core/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "core/login.html")

def redirect_by_role(user):
    if user.role == User.Role.TEACHER:
        return redirect('dashboard')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                return redirect('login')
            except Exception as e:
                print("--- DB ERROR TRACEBACK ---")
                traceback.print_exc()
                print("--------------------------")
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'core/register.html', {'form': form})