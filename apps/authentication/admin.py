from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UserModelAdmin(UserAdmin):
    model = User
    list_display = ['id','email','is_active','is_staff','is_superuser', 'user_type']
    list_filter=['is_superuser']
    search_fields = ('email','first_name')
    ordering = ('email','id')
    filter_horizontal = ('groups', 'user_permissions') 
    readonly_fields = ('date_joined', 'date_updated')
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name','last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type','groups', 'user_permissions' )}),
        ('Important dates', {'fields': ('last_login','date_joined', 'date_updated' )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

# register User model in admin panel
admin.site.register(User,UserModelAdmin)    