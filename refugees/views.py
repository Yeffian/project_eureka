from django.shortcuts import render

def landing(request):
    return render(request, "refugees/landing.html", {"current_page": "refugees"})