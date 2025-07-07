from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_vendor', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_vendor', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone_number', 'date_of_birth', 'is_vendor')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'phone_number', 'date_of_birth', 'is_vendor')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
