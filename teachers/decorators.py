from functools import wraps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def teacher_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != "TEACHER":
            messages.error(request, "That page is only available to teachers.")
            return redirect("core:home")
        return view_func(request, *args, **kwargs)
    return wrapper