from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'tenant', 'is_active']
    list_filter = ['role', 'tenant', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'tenant', 'phone')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'tenant', 'phone')}),
    )
