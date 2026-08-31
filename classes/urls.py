from django.urls import path
from . import views

app_name = "classes"

urlpatterns = [
    path("assignments/<int:assignment_id>/toggle/", views.toggle_assignment, name="toggle_assignment"),
]