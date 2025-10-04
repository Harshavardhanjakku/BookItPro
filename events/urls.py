from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Event URLs
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('<int:event_id>/delete/', views.event_delete, name='event_delete'),
    
    # Event Type URLs
    path('types/', views.event_type_list, name='event_type_list'),
    path('types/create/', views.event_type_create, name='event_type_create'),
    path('types/<int:event_type_id>/edit/', views.event_type_edit, name='event_type_edit'),
    path('types/<int:event_type_id>/delete/', views.event_type_delete, name='event_type_delete'),
    
    # API URLs
    path('api/stats/', views.event_stats_api, name='event_stats_api'),
]
