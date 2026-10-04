from django.urls import path
from . import views

app_name = "teachers"

urlpatterns = [
    path("", views.landing, name="landing"),
    # path("resources/", views.resources, name="resources"),
    path("resources/", views.resources, name="resources"),
]
