from django.contrib import admin

from .models import User
# Register your models here.
admin.site.register(User)

'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Campos adicionales', {'fields': ('phone', 'is_manager')}),
    )'''