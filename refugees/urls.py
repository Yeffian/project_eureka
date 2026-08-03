from django.urls import path
from . import views

app_name = "refugees"

urlpatterns = [
    path("", views.landing, name="landing"),
]