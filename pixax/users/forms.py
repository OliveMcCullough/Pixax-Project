from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import models

from .models import User


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email")


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(help_text="150 characters or fewer. Letters, digits and @/./+/-/_ only.", max_length=150)
    email = forms.EmailField(help_text="Please enter an email address you can be reached with.")
    password1 = forms.CharField(widget=forms.PasswordInput, 
    help_text="Your password can’t be too similar to your other personal information, contain less than 8 characters, be a commonly used password, or be entirely numeric.",
    label="Password")

    class Meta:
        model = User
        fields = ('username', 'email')