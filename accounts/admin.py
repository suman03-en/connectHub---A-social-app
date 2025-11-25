from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id','email','username','is_staff','is_active')
    list_filter=('is_staff','is_active')
    fieldsets = (
        (None,{'fields':('email','password')}),
        ('Personal info',{'fields':('username','first_name','last_name','bio','profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

admin.site.register(CustomUser,CustomUserAdmin)