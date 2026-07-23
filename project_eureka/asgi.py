"""ASGI config for project_eureka."""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_eureka.settings")

application = get_asgi_application()
