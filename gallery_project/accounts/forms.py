# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Обязательное поле.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Обязательное поле.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
