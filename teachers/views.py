"""Teacher views: guest landing and (mock) signed-in dashboard.

Since this is a UI-only migration, `signed_in` is a plain context flag rather
than a real auth check. The landing page passes `signed_in=False`, the
dashboard passes `signed_in=True`; the header partial reads that to swap
between the Sign-in button and the user chip.
"""

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render
from classes.models import Course, Assignment

def landing(request):
    return render(request, "teachers/landing.html", {
        "current_page": "teachers",
        "signed_in": False,
    })
@login_required
def dashboard(request):
    teacher = request.user

    # All courses this teacher runs, with lesson counts annotated in one query
    courses = (
        Course.objects
        .filter(teacher=teacher)
        .annotate(
            total_lessons=Count("lessons", distinct=True),
            completed_lessons=Count("lessons", filter=Q(lessons__is_complete=True), distinct=True),
            student_count=Count("enrollments", distinct=True),
        )
        .order_by("name")
    )

    # Pending assignments across all this teacher's courses (the to-do widget)
    pending_assignments = (
        Assignment.objects
        .filter(course__teacher=teacher, is_done=False)
        .select_related("course")
        .order_by("due_date")
    )

    context = {
        "current_page": "teachers",
        "signed_in": True,
        "display_name": teacher.get_short_name() or teacher.username,
        "avatar_letter": (teacher.get_short_name() or teacher.username)[:1].upper(),
        "courses": courses,
        "pending_assignments": pending_assignments,
        "course_count": courses.count(),
        "pending_count": pending_assignments.count(),
    }
    return render(request, "teachers/dashboard.html", context)

def resources(request):
    return render(request, "teachers/resources.html")