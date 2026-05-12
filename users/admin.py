from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # This tells the admin which fields to display in the list view
    list_display = ['id','email', 'first_name', 'last_name', 'bio', 'created_at']
    
    # This ensures the "Add User" and "Change User" forms use your fields
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio',)}), # Add your custom 'bio' field here
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'email', 'bio')}),
    )
    
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
