from django.shortcuts import render

def landing(request):
    return render(request, "refugees/landing.html", {"current_page": "refugees"})

def dashboard(request):
    return render(request, "refugees/dashboard.html", {
        "current_page": "refugees",
        "signed_in": True,
        "display_name": "Amira",
        "avatar_letter": "A",
    })