from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Event URLs will be added here
    path('', views.event_list, name='event_list'),
]
