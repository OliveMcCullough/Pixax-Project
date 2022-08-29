from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms
from django.db import models
import uuid

from .models import User
from main.services import remove_exif


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


class ProfileUsernameEditForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username']


class ProfilePicEditForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'] = forms.ImageField(label="", required=True, widget=forms.FileInput)

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data['profile_pic']
        if profile_pic == None:
            raise ValidationError("Please provide a new picture for your profile.")
        unique_base_file_name = str(uuid.uuid4())
        data = remove_exif(profile_pic, unique_base_file_name, "pictures/")
        return data