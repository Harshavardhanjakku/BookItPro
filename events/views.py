from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Event, EventType
from .forms import EventForm, EventTypeForm, EventSearchForm
from bookitpro_project.multitenant import get_current_tenant
from accounts.models import User
import json


@login_required
def event_list(request):
    """List all events for the current tenant"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    # Get search form
    search_form = EventSearchForm(request.GET)
    events = Event.objects.filter(tenant_schema=current_tenant.slug)
    
    # Apply search filters
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        search_field = search_form.cleaned_data.get('search_field', 'title')
        event_type_id = search_form.cleaned_data.get('event_type')
        date_from = search_form.cleaned_data.get('date_from')
        date_to = search_form.cleaned_data.get('date_to')
        price_max = search_form.cleaned_data.get('price_max')
        
        if search_query:
            if search_field == 'title':
                events = events.filter(title__icontains=search_query)
            elif search_field == 'description':
                events = events.filter(description__icontains=search_query)
            elif search_field == 'location':
                events = events.filter(location__icontains=search_query)
        
        if event_type_id and event_type_id != 'all':
            events = events.filter(event_type_id=event_type_id)
        
        if date_from:
            events = events.filter(start_date__date__gte=date_from)
        
        if date_to:
            events = events.filter(start_date__date__lte=date_to)
        
        if price_max:
            events = events.filter(price__lte=price_max)
    
    # Order by start date
    events = events.order_by('start_date')
    
    # Pagination
    paginator = Paginator(events, 12)  # 12 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'events': page_obj,
        'search_form': search_form,
        'tenant': current_tenant,
        'total_events': events.count(),
    }
    
    return render(request, 'events/event_list.html', context)


@login_required
def event_detail(request, event_id):
    """Display event details"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    event = get_object_or_404(Event, id=event_id, tenant_schema=current_tenant.slug)
    
    # Get booking count for this event
    booking_count = 0
    if hasattr(event, 'bookings'):
        booking_count = event.bookings.filter(status='confirmed').count()
    
    available_spots = event.capacity - booking_count
    
    context = {
        'event': event,
        'booking_count': booking_count,
        'available_spots': available_spots,
        'tenant': current_tenant,
        'can_book': available_spots > 0 and event.is_active and event.start_date > timezone.now(),
    }
    
    return render(request, 'events/event_detail.html', context)


@login_required
def event_create(request):
    """Create a new event"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    # Check if user can create events
    if not request.user.is_organizer():
        messages.error(request, 'You do not have permission to create events.')
        return redirect('events:event_list')
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.tenant = current_tenant
            event.save()
            messages.success(request, f'Event "{event.title}" created successfully!')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'tenant': current_tenant,
        'action': 'Create',
    }
    
    return render(request, 'events/event_form.html', context)


@login_required
def event_edit(request, event_id):
    """Edit an existing event"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    # Check if user can edit events
    if not request.user.is_organizer():
        messages.error(request, 'You do not have permission to edit events.')
        return redirect('events:event_list')
    
    event = get_object_or_404(Event, id=event_id, tenant_schema=current_tenant.slug)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.title}" updated successfully!')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'tenant': current_tenant,
        'action': 'Edit',
    }
    
    return render(request, 'events/event_form.html', context)


@login_required
def event_delete(request, event_id):
    """Delete an event"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    # Check if user can delete events
    if not request.user.is_organizer():
        messages.error(request, 'You do not have permission to delete events.')
        return redirect('events:event_list')
    
    event = get_object_or_404(Event, id=event_id, tenant_schema=current_tenant.slug)
    
    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f'Event "{event_title}" deleted successfully!')
        return redirect('events:event_list')
    
    context = {
        'event': event,
        'tenant': current_tenant,
    }
    
    return render(request, 'events/event_confirm_delete.html', context)


@login_required
def event_type_list(request):
    """List all event types for the current tenant"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    # Check if user can manage event types
    if not request.user.is_organizer():
        messages.error(request, 'You do not have permission to manage event types.')
        return redirect('events:event_type_list')
    
    event_types = EventType.objects.filter(tenant_schema=current_tenant.slug).order_by('name')
    
    context = {
        'event_types': event_types,
        'tenant': current_tenant,
    }
    
    return render(request, 'events/event_type_list.html', context)


@login_required
def event_type_create(request):
    """Create a new event type"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    # Check if user can manage event types
    if not request.user.is_organizer():
        messages.error(request, 'You do not have permission to manage event types.')
        return redirect('events:event_type_list')
    
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            event_type = form.save(commit=False)
            event_type.save()
            messages.success(request, f'Event type "{event_type.name}" created successfully!')
            return redirect('events:event_type_list')
    else:
        form = EventTypeForm()
    
    context = {
        'form': form,
        'tenant': current_tenant,
        'action': 'Create',
    }
    
    return render(request, 'events/event_type_form.html', context)


@login_required
def event_type_edit(request, event_type_id):
    """Edit an existing event type"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    # Check if user can manage event types
    if not request.user.is_organizer():
        messages.error(request, 'You do not have permission to manage event types.')
        return redirect('events:event_type_list')
    
    event_type = get_object_or_404(EventType, id=event_type_id, tenant_schema=current_tenant.slug)
    
    if request.method == 'POST':
        form = EventTypeForm(request.POST, instance=event_type)
        if form.is_valid():
            event_type = form.save()
            messages.success(request, f'Event type "{event_type.name}" updated successfully!')
            return redirect('events:event_type_list')
    else:
        form = EventTypeForm(instance=event_type)
    
    context = {
        'form': form,
        'event_type': event_type,
        'tenant': current_tenant,
        'action': 'Edit',
    }
    
    return render(request, 'events/event_type_form.html', context)


@login_required
def event_type_delete(request, event_type_id):
    """Delete an event type"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    # Check if user can manage event types
    if not request.user.is_organizer():
        messages.error(request, 'You do not have permission to manage event types.')
        return redirect('events:event_type_list')
    
    event_type = get_object_or_404(EventType, id=event_type_id, tenant_schema=current_tenant.slug)
    
    # Check if event type is being used
    events_using_type = Event.objects.filter(event_type=event_type, tenant_schema=current_tenant.slug)
    if events_using_type.exists():
        messages.error(request, f'Cannot delete event type "{event_type.name}" because it is being used by {events_using_type.count()} event(s).')
        return redirect('events:event_type_list')
    
    if request.method == 'POST':
        event_type_name = event_type.name
        event_type.delete()
        messages.success(request, f'Event type "{event_type_name}" deleted successfully!')
        return redirect('events:event_type_list')
    
    context = {
        'event_type': event_type,
        'tenant': current_tenant,
    }
    
    return render(request, 'events/event_type_confirm_delete.html', context)


# API Endpoints for AJAX requests
@login_required
@require_http_methods(["GET"])
def event_stats_api(request):
    """API endpoint to get event statistics"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        return JsonResponse({'error': 'No tenant context found'}, status=400)
    
    # Check if user can view stats
    if not request.user.is_organizer():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        total_events = Event.objects.filter(tenant_schema=current_tenant.slug).count()
        active_events = Event.objects.filter(tenant_schema=current_tenant.slug, is_active=True).count()
        upcoming_events = Event.objects.filter(
            tenant_schema=current_tenant.slug,
            start_date__gt=timezone.now()
        ).count()
        
        # Get event types with counts
        event_types = EventType.objects.filter(tenant_schema=current_tenant.slug).annotate(
            event_count=Count('events')
        ).order_by('-event_count')
        
        event_type_data = [
            {
                'name': et.name,
                'count': et.event_count,
                'icon': et.icon
            }
            for et in event_types
        ]
        
        return JsonResponse({
            'success': True,
            'stats': {
                'total_events': total_events,
                'active_events': active_events,
                'upcoming_events': upcoming_events,
                'event_types': event_type_data
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)