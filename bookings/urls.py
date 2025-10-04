from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Booking URLs will be added here
    path('', views.booking_list, name='booking_list'),
]
