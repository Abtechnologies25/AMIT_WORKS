from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # Show these fields in admin list view
    list_display = ('username', 'employee_name', 'department', 'branch', 'is_team_leader', 'is_approved', 'is_staff')
    list_filter = ('department', 'branch', 'is_team_leader', 'is_approved')

    # Fields to search
    search_fields = ('username', 'employee_name')

    # Editable fields in detail view
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('employee_name', 'department', 'branch', 'is_team_leader', 'is_approved')}),
    )

    # Fields when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('employee_name', 'department', 'branch', 'is_team_leader', 'is_approved')}),
    )

admin.site.register(User, CustomUserAdmin)