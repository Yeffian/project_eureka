from django.urls import path
from . import views

app_name = "teachers"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("resources/", views.resources, name="resources")
]
