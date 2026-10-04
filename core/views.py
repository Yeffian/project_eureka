"""Core views: simple template renders for the marketing/public pages.

The `current_page` context value drives the "active" state (bold + always-on squiggle)
on the corresponding link in the header partial.
"""

from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.shortcuts import render
from django.urls import reverse
from .models import *

def home(request):
    return render(request, "core/home.html", {"current_page": "home"})


def about(request):
    return render(request, "core/about.html", {"current_page": "about"})


def faq(request):
    return render(request, "core/faq.html", {"current_page": "faq"})

def contact(request):
    return render(request, "core/contact.html", {"current_page": "contact"})
