from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Tenant(models.Model):
    """Organization/Tenant model for multitenant architecture"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="URL-friendly name")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
    
    def __str__(self):
        return self.name


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    ROLE_CHOICES = [
        ('admin', 'Organizer Admin'),
        ('manager', 'Event Manager'),
        ('attendee', 'Attendee'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attendee')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    def is_organizer(self):
        return self.role in ['admin', 'manager']
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_manager(self):
        return self.role == 'manager'
    
    def is_attendee(self):
        return self.role == 'attendee'
