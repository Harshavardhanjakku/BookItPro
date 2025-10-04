from django.db import models
from django.utils import timezone
from accounts.models import User
from events.models import Event
from bookitpro_project.multitenant import TenantAwareModel


class Booking(TenantAwareModel):
    """Booking model for event reservations"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    
    # Booking details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(default=timezone.now)
    confirmation_code = models.CharField(max_length=20, unique=True, blank=True)
    
    # Additional information
    notes = models.TextField(blank=True)
    special_requirements = models.TextField(blank=True)
    
    # Payment information
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ], default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        unique_together = ['event', 'user', 'tenant_schema']  # One booking per user per event per tenant
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.event.title}"
    
    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = self.generate_confirmation_code()
        super().save(*args, **kwargs)
    
    def generate_confirmation_code(self):
        """Generate a unique confirmation code"""
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    def can_cancel(self):
        """Check if booking can be cancelled"""
        return self.status in ['pending', 'confirmed'] and not self.event.is_past_event()
    
    def is_confirmed(self):
        """Check if booking is confirmed"""
        return self.status == 'confirmed'
    
    def is_cancelled(self):
        """Check if booking is cancelled"""
        return self.status == 'cancelled'


class BookingHistory(TenantAwareModel):
    """Track booking status changes"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reason = models.TextField(blank=True)
    changed_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Booking History"
        verbose_name_plural = "Booking Histories"
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"{self.booking} - {self.old_status} → {self.new_status}"
