from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.Role.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Select your role in Project Eureka"
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'role')