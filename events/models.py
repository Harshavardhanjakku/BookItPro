from django.db import models
from django.utils import timezone
from accounts.models import Tenant
from bookitpro_project.multitenant import TenantAwareModel


class EventType(TenantAwareModel):
    """Event type model (hackathon, webinar, concert, etc.)"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    class Meta:
        verbose_name = "Event Type"
        verbose_name_plural = "Event Types"
        unique_together = ['name', 'tenant_schema']  # Unique within tenant
    
    def __str__(self):
        return self.name


class Event(TenantAwareModel):
    """Event model for the booking system"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    
    # Event details
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_active = models.BooleanField(default=True, help_text="Whether the event is active and visible to users")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    requirements = models.TextField(blank=True, help_text="Special requirements or instructions")
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.tenant.name})"
    
    def get_available_spots(self):
        """Calculate available spots for booking"""
        booked_count = self.bookings.filter(status__in=['confirmed', 'pending']).count()
        return max(0, self.capacity - booked_count)
    
    def is_fully_booked(self):
        """Check if event is fully booked"""
        return self.get_available_spots() == 0
    
    def is_past_event(self):
        """Check if event has already ended"""
        return timezone.now() > self.end_date
    
    def is_upcoming(self):
        """Check if event is upcoming"""
        return timezone.now() < self.start_date
