from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request, "students/landing.html", {"current_page": "students"})
