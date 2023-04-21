from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import *


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('mobile_number', 'email', 'name', 'family', 'gender', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin')
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('personal_info', {'fields': ('email', 'name', 'family', 'gender', 'active_code')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {'fields': ('mobile_number', 'email', 'name', 'family', 'gender', 'is_active', 'is_admin', 'password1', 'password2')}),
    )

    search_fields = ('mobile_number',)
    ordering = ('mobile_number',)
    filter_horizontal = ('groups', 'user_permissions')

# ===================================================================================
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phon_number')

# ===================================================================================
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'is_seen', 'register_date')
    ordering = ('register_date',)


