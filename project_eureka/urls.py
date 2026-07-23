"""Top-level URL routing.

Flat URL structure:
    /                 → core:home
    /about/           → core:about
    /faq/             → core:faq
    /teachers/        → teachers:landing
    /teachers/dashboard/ → teachers:dashboard
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),

    path("teachers/", include("teachers.urls")),
    path("", include("core.urls")),  # keep last so it doesn't shadow other prefixes
]
