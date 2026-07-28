from django.db import models  # noqa: F401
from django.contrib.auth.models import AbstractUser

# No models yet — the core app is currently just template views.

class User(AbstractUser):
    class Role(models.TextChoices):
        TEACHER = 'TEACHER', 'Teacher'
        CCA_MEMBER = 'CCA_MEMBER', 'CCA Member'
        REFUGEE_STUDENT = 'REFUGEE_STUDENT', 'Refugee Student'
        STUDENT = 'STUDENT', 'Student'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    
    role = models.CharField(
        max_length=100,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="Select your user role"
    )

    # Note: Using standard Django field names 'first_name' and 'last_name'
    # 'username' and 'password' are automatically required by AbstractUser


    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"