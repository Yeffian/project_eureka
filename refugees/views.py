from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie


def landing(request):
    return render(request, "refugees/landing.html", {"current_page": "refugees"})