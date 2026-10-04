from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("teachers/", include("teachers.urls")),
    path("students/", include("students.urls")),
    path("refugees/", include("refugees.urls")),
    path("", include("core.urls")),  # keep last so it doesn't shadow other prefixes
]
