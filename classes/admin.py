from django.contrib import admin
from .models import Course, Enrollment, Lesson, Assignment, AssignmentCompletion


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 3                      # show 3 blank lesson rows by default
    fields = ("order", "title", "session_date", "is_complete")


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    fields = ("student", "enrolled_at")
    readonly_fields = ("enrolled_at",)


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 2
    fields = ("title", "due_date", "is_done")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "teacher", "color", "created_at")
    list_filter = ("subject", "teacher")
    search_fields = ("name", "subject")
    inlines = [LessonInline, EnrollmentInline, AssignmentInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "session_date", "is_complete")
    list_filter = ("is_complete", "course")
    search_fields = ("title",)
    list_editable = ("is_complete",)     # toggle completion straight from the list


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "due_date", "is_done")
    list_filter = ("is_done", "course")
    search_fields = ("title",)
    list_editable = ("is_done",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at")
    list_filter = ("course",)
    

@admin.register(AssignmentCompletion)
class AssignmentCompletionAdmin(admin.ModelAdmin):
    list_display = ("student", "assignment", "is_done", "completed_at")
    list_filter = ("is_done", "assignment__course")
    search_fields = ("student__username", "assignment__title")
    list_editable = ("is_done",)