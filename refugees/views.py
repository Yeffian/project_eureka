from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from classes.models import Assignment, AssignmentCompletion
from forum.models import Thread

def landing(request):
    return render(request, "refugees/landing.html", {"current_page": "refugees"})


@ensure_csrf_cookie
@login_required
def dashboard(request):
    student = request.user

    # Courses this student is enrolled in
    enrolled_course_ids = student.enrollments.values_list("course_id", flat=True)

    # All assignments across those courses
    assignments = (
        Assignment.objects
        .filter(course_id__in=enrolled_course_ids)
        .select_related("course", "course__teacher")
        .order_by("title")
    )

    # Lazy get-or-create: ensure a completion record exists per assignment for this student
    for assignment in assignments:
        AssignmentCompletion.objects.get_or_create(
            assignment=assignment,
            student=student,
            defaults={"is_done": False},
        )

    # Fetch the student's completion records, joined to assignment + course + teacher
    completions = (
        AssignmentCompletion.objects
        .filter(student=student, assignment__course_id__in=enrolled_course_ids)
        .select_related("assignment", "assignment__course", "assignment__course__teacher")
        .order_by("assignment__title")
    )

    pending_count = completions.filter(is_done=False).count()

    recent_threads = (
        Thread.objects
        .select_related("category", "author")
        .annotate(reply_count=Count("replies"))
        .order_by("-created_at")[:3]
    )

    context = {
        "current_page": "refugees",
        "signed_in": True,
        "display_name": student.get_short_name() or student.username,
        "avatar_letter": (student.get_short_name() or student.username)[:1].upper(),
        "completions": completions,
        "pending_count": pending_count,
        "recent_threads": recent_threads,
    }
    return render(request, "refugees/dashboard.html", context)