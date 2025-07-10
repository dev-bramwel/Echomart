from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'



class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    
    list_display = ('email', 'username','full_name', 'phone_number', 'is_vendor', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_vendor', 'created_at')
    search_fields = ('email', 'full_name', 'phone_number', 'username')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_vendor', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'date_of_birth', 'is_vendor', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
