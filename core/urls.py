from django.urls import path, include
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("register/", views.register, name="register"),
    path("login_view/", views.login_view, name="login_view"),
    path("logout_view/", views.logout_view, name="logout_view"),
]
