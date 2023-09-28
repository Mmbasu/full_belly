from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'username', 'last_name', 'role', 'photo', 'phone', 'delete_account_code', 'instagram_link', 'facebook_link', 'twitter_link', 'is_staff', 'is_active', 'password', 'temporary_password', 'date_joined', 'failed_login_attempts', 'last_login_attempt_exceeded')
    list_filter = ('email', 'is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
