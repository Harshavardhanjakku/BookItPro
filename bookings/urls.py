from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Booking URLs
    path('', views.booking_list, name='booking_list'),
    path('create/<int:event_id>/', views.booking_create, name='booking_create'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('<int:booking_id>/update/', views.booking_update, name='booking_update'),
    
    # Admin URLs
    path('admin/', views.admin_booking_list, name='admin_booking_list'),
    
    # API URLs
    path('api/stats/', views.booking_stats_api, name='booking_stats_api'),
]
