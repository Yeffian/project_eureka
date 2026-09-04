import json
from django.contrib.auth import get_user_model
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Assignment, AssignmentCompletion
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Course, Lesson, Assignment
from .forms import LessonForm, AssignmentForm
from teachers.decorators import teacher_required


@login_required
@require_POST
def toggle_assignment(request, assignment_id):
    # Only let a teacher toggle assignments in their own courses
    try:
        assignment = Assignment.objects.get(pk=assignment_id, course__teacher=request.user)
    except Assignment.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    data = json.loads(request.body)
    assignment.is_done = bool(data.get("is_done"))
    assignment.save(update_fields=["is_done"])

    return JsonResponse({"id": assignment.pk, "is_done": assignment.is_done})

@login_required
@require_POST
def toggle_completion(request, completion_id):
    try:
        completion = AssignmentCompletion.objects.get(pk=completion_id, student=request.user)
    except AssignmentCompletion.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    data = json.loads(request.body)
    completion.is_done = bool(data.get("is_done"))
    completion.completed_at = timezone.now() if completion.is_done else None
    completion.save(update_fields=["is_done", "completed_at"])

    return JsonResponse({"id": completion.pk, "is_done": completion.is_done})

def _teacher_course_or_404(request, course_id):
    return get_object_or_404(Course, pk=course_id, teacher=request.user)

@login_required
@require_POST
def create_lesson(request, course_id):
    course = _teacher_course_or_404(request, course_id)
    form = LessonForm(request.POST)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.course = course
        lesson.save()
    return redirect("teachers:course_detail", course_id=course.pk)

@login_required
@require_POST
def toggle_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id, course__teacher=request.user)
    lesson.is_complete = not lesson.is_complete
    lesson.save(update_fields=["is_complete"])
    return redirect("teachers:course_detail", course_id=lesson.course_id)


@login_required
@require_POST
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id, course__teacher=request.user)
    course_id = lesson.course_id
    lesson.delete()
    return redirect("teachers:course_detail", course_id=course_id)

@login_required
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id, course__teacher=request.user)

    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment, teacher=request.user)
        if form.is_valid():
            form.save()
            return redirect("teachers:course_detail", course_id=assignment.course_id)
    else:
        form = AssignmentForm(instance=assignment, teacher=request.user)

    return render(request, "teachers/assignment_form.html", {
        "current_page": "teachers",
        "signed_in": True,
        "display_name": request.user.get_short_name() or request.user.username,
        "avatar_letter": (request.user.get_short_name() or request.user.username)[:1].upper(),
        "form": form,
        "editing": True,
        "assignment": assignment,
    })

@login_required
@require_POST
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id, course__teacher=request.user)
    course_id = assignment.course_id
    assignment.delete()
    return redirect("teachers:course_detail", course_id=course_id)

User = get_user_model()
ENROLLABLE_ROLES = ["CCA_MEMBER", "REFUGEE_STUDENT", "STUDENT"]


@teacher_required
def manage_students(request, course_id):
    course = get_object_or_404(Course, pk=course_id, teacher=request.user)

    if request.method == "POST":
        student_id = request.POST.get("student")
        if student_id:
            # Only enroll a user who is eligible and not already enrolled
            student = User.objects.filter(
                pk=student_id,
                role__in=ENROLLABLE_ROLES,
            ).first()
            if student:
                Enrollment.objects.get_or_create(course=course, student=student)
        return redirect("classes:manage_students", course_id=course.pk)

    enrollments = course.enrollments.select_related("student").order_by("student__username")

    # Eligible students NOT already enrolled in this course
    enrolled_ids = enrollments.values_list("student_id", flat=True)
    available_students = (
        User.objects
        .filter(role__in=ENROLLABLE_ROLES)
        .exclude(pk__in=enrolled_ids)
        .order_by("username")
    )

    return render(request, "teachers/manage_students.html", {
        "current_page": "teachers",
        "signed_in": True,
        "display_name": request.user.get_short_name() or request.user.username,
        "avatar_letter": (request.user.get_short_name() or request.user.username)[:1].upper(),
        "course": course,
        "enrollments": enrollments,
        "available_students": available_students,
    })

@login_required
@require_POST
def remove_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(
        Enrollment,
        pk=enrollment_id,
        course__teacher=request.user,
    )
    course_id = enrollment.course_id
    enrollment.delete()
    return redirect("classes:manage_students", course_id=course_id)