from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

def landing(request):
    return render(request, "teachers/landing.html")

def resources(request):
    return render(request, "teachers/resources.html")

