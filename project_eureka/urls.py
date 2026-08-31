from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),

    path("teachers/", include("teachers.urls")),
    path("students/", include("students.urls")),
    path("refugees/", include("refugees.urls")),
    path("forum/", include("forum.urls")),
    path("classes/", include("classes.urls")),
    path("", include("core.urls")),  # keep last so it doesn't shadow other prefixes
]
