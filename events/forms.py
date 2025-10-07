from django import forms
from django.core.exceptions import ValidationError
from .models import Event, EventType
from bookitpro_project.multitenant import get_current_tenant
from datetime import datetime, date


class EventTypeForm(forms.ModelForm):
    """Form for creating and editing event types"""
    
    class Meta:
        model = EventType
        fields = ['name', 'description', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event type name (e.g., Hackathon, Webinar, Concert)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe this event type'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter icon class (e.g., fas fa-code, fas fa-video)'
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip().title()
            # Check for uniqueness within current tenant
            current_tenant = get_current_tenant()
            if current_tenant:
                existing = EventType.objects.filter(
                    name__iexact=name,
                    tenant=current_tenant
                ).exclude(pk=self.instance.pk if self.instance else None)
                if existing.exists():
                    raise ValidationError(f"Event type '{name}' already exists in your organization.")
        return name


class EventForm(forms.ModelForm):
    """Form for creating and editing events"""
    
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type', 'start_date', 'end_date',
            'location', 'capacity', 'price', 'image', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your event in detail'
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event location or venue'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Maximum number of attendees'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Event price (0 for free events)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter event types by current tenant
        current_tenant = get_current_tenant()
        if current_tenant:
            self.fields['event_type'].queryset = EventType.objects.filter(
                tenant=current_tenant
            )
        else:
            self.fields['event_type'].queryset = EventType.objects.none()
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError("End date must be after start date.")
            
            if start_date.date() < date.today():
                raise ValidationError("Start date cannot be in the past.")
        
        return cleaned_data
    
    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity and capacity < 1:
            raise ValidationError("Capacity must be at least 1.")
        return capacity
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise ValidationError("Price cannot be negative.")
        return price


class EventSearchForm(forms.Form):
    """Form for searching and filtering events"""
    
    SEARCH_CHOICES = [
        ('title', 'Title'),
        ('description', 'Description'),
        ('location', 'Location'),
    ]
    
    TYPE_CHOICES = [
        ('all', 'All Types'),
    ]
    
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search events...'
        })
    )
    
    search_field = forms.ChoiceField(
        choices=SEARCH_CHOICES,
        required=False,
        initial='title',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    event_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
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
    
    price_max = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': 'Maximum price'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add event types for current tenant
        current_tenant = get_current_tenant()
        if current_tenant:
            event_types = EventType.objects.filter(tenant=current_tenant)
            type_choices = [('all', 'All Types')]
            type_choices.extend([(et.id, et.name) for et in event_types])
            self.fields['event_type'].choices = type_choices
