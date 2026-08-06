from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_thread, name="new_thread"),
    path("<slug:category_slug>/", views.category, name="category"),
    path("<slug:category_slug>/<int:thread_id>/", views.thread, name="thread"),
]