"""WSGI config for project_eureka."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_eureka.settings")

application = get_wsgi_application()
