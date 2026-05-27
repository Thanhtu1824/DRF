from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'phone',
        'role',
        'status',
        'is_staff',
        'is_active',
    )
    search_fields = (
        'username',
        'email',
        'phone',
    )
    list_filter = (
        'role',
        'status',
        'is_staff',
        'is_active',
    )
    ordering = ('id',)
    fieldsets = UserAdmin.fieldsets + (  # type: ignore[operator]
        (
            'Custom fields',
            {
                'fields': (
                    'phone',
                    'role',
                    'avatar',
                    'status',
                ),
            },
        ),
    )
