from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie


def landing(request):
    if request.user.is_authenticated and request.user.role == "REFUGEE_STUDENT":
        return redirect("refugees:dashboard")
    return render(request, "refugees/landing.html", {"current_page": "refugees"})