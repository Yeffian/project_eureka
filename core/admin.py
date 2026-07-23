from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register models here when the core app grows models of its own.

admin.site.register(User, UserAdmin)
