from django.shortcuts import render
from django.http import HttpResponse

def booking_list(request):
    """Booking list view"""
    return HttpResponse("Bookings list - Coming soon!")
