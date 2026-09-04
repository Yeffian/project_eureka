from django.urls import path
from . import views

app_name = "teachers"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("resources/", views.resources, name="resources"),
    path("classrooms/", views.classrooms, name="classrooms"),
    path("classrooms/new/", views.create_course, name="create_course"),
    path("classrooms/<int:course_id>/", views.course_detail, name="course_detail"),
    path("assignments/new/", views.create_assignment, name="create_assignment"),
    path("classrooms/<int:course_id>/edit/", views.edit_course, name="edit_course"),
    path("classrooms/<int:course_id>/delete/", views.delete_course, name="delete_course"),
]
