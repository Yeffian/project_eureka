from django.urls import path
from . import views

app_name = "classes"

urlpatterns = [
    path("assignments/<int:assignment_id>/toggle/", views.toggle_assignment, name="toggle_assignment"),
    path("completions/<int:completion_id>/toggle/", views.toggle_completion, name="toggle_completion"),
    path("courses/<int:course_id>/lessons/new/", views.create_lesson, name="create_lesson"),
    path("lessons/<int:lesson_id>/toggle/", views.toggle_lesson, name="toggle_lesson"),
    path("lessons/<int:lesson_id>/delete/", views.delete_lesson, name="delete_lesson"),
    path("assignments/<int:assignment_id>/edit/", views.edit_assignment, name="edit_assignment"),
    path("assignments/<int:assignment_id>/delete/", views.delete_assignment, name="delete_assignment"),
    path("courses/<int:course_id>/students/", views.manage_students, name="manage_students"),
    path("enrollments/<int:enrollment_id>/remove/", views.remove_enrollment, name="remove_enrollment"),
]