"""Teacher views: guest landing and (mock) signed-in dashboard.

Since this is a UI-only migration, `signed_in` is a plain context flag rather
than a real auth check. The landing page passes `signed_in=False`, the
dashboard passes `signed_in=True`; the header partial reads that to swap
between the Sign-in button and the user chip.
"""

from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from classes.forms import CourseForm, AssignmentForm
from classes.models import Course, Assignment
from forum.models import Thread
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from teachers.decorators import teacher_required

def landing(request):
    return render(request, "teachers/landing.html", {
        "current_page": "teachers",
        "signed_in": False,
    })

@teacher_required
@ensure_csrf_cookie
def dashboard(request):
    teacher = request.user

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

    pending_assignments = (
        Assignment.objects
        .filter(course__teacher=teacher, is_done=False)
        .select_related("course")
        .order_by("due_date")
    )

    recent_threads = (
        Thread.objects
        .select_related("category", "author")
        .annotate(reply_count=Count("replies"))
        .order_by("-created_at")[:3]
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
        "recent_threads": recent_threads,   
}


    return render(request, "teachers/dashboard.html", context)

@teacher_required
def resources(request):
    return render(request, "teachers/resources.html")

@teacher_required
def classrooms(request):
    courses = (
        Course.objects
        .filter(teacher=request.user)
        .annotate(
            total_lessons=Count("lessons", distinct=True),
            completed_lessons=Count("lessons", filter=Q(lessons__is_complete=True), distinct=True),
            student_count=Count("enrollments", distinct=True),
            assignment_count=Count("assignments", distinct=True),
        )
        .order_by("name")
    )
    return render(request, "teachers/classrooms.html", {
        "current_page": "teachers",
        "signed_in": True,
        "display_name": request.user.get_short_name() or request.user.username,
        "avatar_letter": (request.user.get_short_name() or request.user.username)[:1].upper(),
        "courses": courses,
    })

@teacher_required
def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user      # set owner before saving
            course.save()
            return redirect("teachers:classrooms")
    else:
        form = CourseForm()

    return render(request, "teachers/course_form.html", {
        "current_page": "teachers",
        "signed_in": True,
        "display_name": request.user.get_short_name() or request.user.username,
        "avatar_letter": (request.user.get_short_name() or request.user.username)[:1].upper(),
        "form": form,
    })

@teacher_required
def create_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, teacher=request.user)
        if form.is_valid():
            form.save()
            return redirect("teachers:classrooms")
    else:
        # Pre-select a course if ?course=<pk> is in the URL (from the hub's per-course button)
        initial = {}
        course_id = request.GET.get("course")
        if course_id:
            initial["course"] = course_id
        form = AssignmentForm(teacher=request.user, initial=initial)

    return render(request, "teachers/assignment_form.html", {
        "current_page": "teachers",
        "signed_in": True,
        "display_name": request.user.get_short_name() or request.user.username,
        "avatar_letter": (request.user.get_short_name() or request.user.username)[:1].upper(),
        "form": form,
    })

@teacher_required
def course_detail(request, course_id):
    # Scope to the teacher's own courses, 404 if it's not theirs
    course = get_object_or_404(Course, pk=course_id, teacher=request.user)

    lessons = course.lessons.order_by("order")
    assignments = course.assignments.order_by("is_done", "due_date")
    enrollments = course.enrollments.select_related("student").order_by("student__username")

    return render(request, "teachers/course_detail.html", {
        "current_page": "teachers",
        "signed_in": True,
        "display_name": request.user.get_short_name() or request.user.username,
        "avatar_letter": (request.user.get_short_name() or request.user.username)[:1].upper(),
        "course": course,
        "lessons": lessons,
        "assignments": assignments,
        "enrollments": enrollments,
    })


@teacher_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id, teacher=request.user)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("teachers:course_detail", course_id=course.pk)
    else:
        form = CourseForm(instance=course)

    return render(request, "teachers/course_form.html", {
        "current_page": "teachers",
        "signed_in": True,
        "display_name": request.user.get_short_name() or request.user.username,
        "avatar_letter": (request.user.get_short_name() or request.user.username)[:1].upper(),
        "form": form,
        "editing": True,
        "course": course,
    })

@teacher_required
@require_POST
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id, teacher=request.user)
    course.delete()
    return redirect("teachers:classrooms")