from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import AdminUserChangeForm, AdminUserCreationForm


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ["email", "username"]

    form = AdminUserChangeForm
    add_form = AdminUserCreationForm

    fieldsets = (
        (None, {'fields': ('email','username')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )

admin.site.register(User, UserAdmin)
