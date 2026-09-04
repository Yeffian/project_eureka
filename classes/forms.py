from django import forms
from .models import Course, Assignment, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "subject", "color"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "doodle-input",
                "placeholder": "e.g. Year 7 English",
            }),
            "subject": forms.TextInput(attrs={
                "class": "doodle-input",
                "placeholder": "e.g. English",
            }),
            "color": forms.Select(
                choices=[
                    ("mint", "Mint"),
                    ("butter", "Butter"),
                    ("blush", "Blush"),
                    ("lilac", "Lilac"),
                    ("sky", "Sky"),
                ],
                attrs={"class": "doodle-select"},
            ),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["course", "title", "due_date"]
        widgets = {
            "course": forms.Select(attrs={"class": "doodle-select"}),
            "title": forms.TextInput(attrs={
                "class": "doodle-input",
                "placeholder": "e.g. Write about your week",
            }),
            "due_date": forms.DateInput(attrs={
                "class": "doodle-input",
                "type": "date",   # native browser date picker
            }),
        }

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the course dropdown to THIS teacher's courses
        if teacher is not None:
            self.fields["course"].queryset = Course.objects.filter(teacher=teacher).order_by("name")


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "order", "session_date"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "doodle-input",
                "placeholder": "e.g. Everyday verbs",
            }),
            "order": forms.NumberInput(attrs={
                "class": "doodle-input",
                "min": "0",
            }),
            "session_date": forms.DateInput(attrs={
                "class": "doodle-input",
                "type": "date",
            }),
        }