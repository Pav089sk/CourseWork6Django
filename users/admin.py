from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

class CustomUserAdmin(UserAdmin):
    filter_horizontal = ('groups', 'user_permissions')

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')

admin.site.register(CustomUser, CustomUserAdmin)
