from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.unregister(User)

# Register the User model with your custom UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Add or override features here, e.g., custom fields, list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')