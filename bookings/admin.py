from django.contrib import admin
from .models import Booking, BookingHistory


class BookingHistoryInline(admin.TabularInline):
    model = BookingHistory
    extra = 0
    readonly_fields = ['changed_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'booking_date', 'confirmation_code', 'payment_status']
    list_filter = ['status', 'payment_status', 'booking_date', 'event__tenant']
    search_fields = ['user__email', 'event__title', 'confirmation_code']
    date_hierarchy = 'booking_date'
    inlines = [BookingHistoryInline]
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('event', 'user', 'status', 'confirmation_code')
        }),
        ('Details', {
            'fields': ('notes', 'special_requirements')
        }),
        ('Payment', {
            'fields': ('amount_paid', 'payment_status')
        }),
    )


@admin.register(BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ['booking', 'old_status', 'new_status', 'changed_by', 'changed_at']
    list_filter = ['new_status', 'changed_at']
    search_fields = ['booking__user__email', 'booking__event__title']
    readonly_fields = ['changed_at']
