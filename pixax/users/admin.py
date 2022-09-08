from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import FriendRequest, Friendship, User
from .forms import AdminUserChangeForm, AdminUserCreationForm

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ["email", "username", "is_active", 'profile_pic']

    form = AdminUserChangeForm
    add_form = AdminUserCreationForm

    fieldsets = (
        (None, {'fields': ('email','username', "is_active", 'profile_pic', 'unique_link_id')}),
    )
    readonly_fields= ("unique_link_id",)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )


class FriendRequestAdmin(admin.ModelAdmin):
    model = FriendRequest


class FriendshipAdmin(admin.ModelAdmin):
    model = Friendship


admin.site.register(User, UserAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Friendship, FriendshipAdmin)
