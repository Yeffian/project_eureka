import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Assignment, AssignmentCompletion


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