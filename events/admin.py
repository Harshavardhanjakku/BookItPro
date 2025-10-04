from django.contrib import admin
from .models import Event, EventType


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'tenant', 'start_date', 'capacity', 'status', 'is_featured']
    list_filter = ['event_type', 'tenant', 'status', 'is_featured', 'start_date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'start_date'
    filter_horizontal = []
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'event_type', 'tenant')
        }),
        ('Event Details', {
            'fields': ('start_date', 'end_date', 'location', 'capacity', 'price')
        }),
        ('Status & Settings', {
            'fields': ('status', 'is_featured', 'requirements')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )
