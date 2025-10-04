from django import forms
from django.core.exceptions import ValidationError
from .models import Booking
from events.models import Event
from bookitpro_project.multitenant import get_current_tenant
from django.utils import timezone


class BookingForm(forms.ModelForm):
    """Form for creating event bookings"""
    
    class Meta:
        model = Booking
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requirements or notes (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        
        if not self.event:
            raise ValidationError("Event is required for booking.")
        
        if not self.user:
            raise ValidationError("User is required for booking.")
        
        # Check if event is active
        if not self.event.is_active:
            raise ValidationError("This event is not active and cannot be booked.")
        
        # Check if event hasn't started yet
        if self.event.start_date <= timezone.now():
            raise ValidationError("This event has already started or ended.")
        
        # Check if user already has a booking for this event
        current_tenant = get_current_tenant()
        if current_tenant:
            existing_booking = Booking.objects.filter(
                event=self.event,
                user=self.user,
                tenant_schema=current_tenant.slug,
                status__in=['confirmed', 'pending']
            ).exists()
            
            if existing_booking:
                raise ValidationError("You already have a booking for this event.")
        
        # Check capacity
        booking_count = Booking.objects.filter(
            event=self.event,
            status='confirmed',
            tenant_schema=current_tenant.slug if current_tenant else ''
        ).count()
        
        if booking_count >= self.event.capacity:
            raise ValidationError("This event is fully booked.")
        
        return cleaned_data


class BookingSearchForm(forms.Form):
    """Form for searching and filtering bookings"""
    
    STATUS_CHOICES = [
        ('all', 'All Statuses'),
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]
    
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by event title...'
        })
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        initial='all',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


class BookingUpdateForm(forms.ModelForm):
    """Form for updating booking status (admin only)"""
    
    class Meta:
        model = Booking
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Update booking notes...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow certain status transitions
        if self.instance and self.instance.pk:
            current_status = self.instance.status
            if current_status == 'cancelled':
                # Can't change from cancelled
                self.fields['status'].choices = [('cancelled', 'Cancelled')]
            elif current_status == 'confirmed':
                # Can only cancel from confirmed
                self.fields['status'].choices = [
                    ('confirmed', 'Confirmed'),
                    ('cancelled', 'Cancelled')
                ]
            elif current_status == 'pending':
                # Can confirm or cancel from pending
                self.fields['status'].choices = [
                    ('pending', 'Pending'),
                    ('confirmed', 'Confirmed'),
                    ('cancelled', 'Cancelled')
                ]
