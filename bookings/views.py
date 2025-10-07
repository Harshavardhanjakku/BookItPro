from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Booking, BookingHistory
from .forms import BookingForm, BookingSearchForm, BookingUpdateForm
from events.models import Event
from bookitpro_project.multitenant import get_current_tenant
from accounts.models import User
import uuid


@login_required
def booking_list(request):
    """List all bookings for the current user"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    # Get search form
    search_form = BookingSearchForm(request.GET)
    bookings = Booking.objects.filter(
        user=request.user,
        tenant=current_tenant
    ).select_related('event', 'event__event_type')
    
    # Apply search filters
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        status = search_form.cleaned_data.get('status')
        date_from = search_form.cleaned_data.get('date_from')
        date_to = search_form.cleaned_data.get('date_to')
        
        if search_query:
            bookings = bookings.filter(event__title__icontains=search_query)
        
        if status and status != 'all':
            bookings = bookings.filter(status=status)
        
        if date_from:
            bookings = bookings.filter(event__start_date__date__gte=date_from)
        
        if date_to:
            bookings = bookings.filter(event__start_date__date__lte=date_to)
    
    # Order by booking date (newest first)
    bookings = bookings.order_by('-booking_date')
    
    # Pagination
    paginator = Paginator(bookings, 10)  # 10 bookings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'bookings': page_obj,
        'search_form': search_form,
        'tenant': current_tenant,
        'total_bookings': bookings.count(),
    }
    
    return render(request, 'bookings/booking_list.html', context)


@login_required
def booking_detail(request, booking_id):
    """Display booking details"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        tenant=current_tenant
    )
    
    # Get booking history
    history = BookingHistory.objects.filter(
        booking=booking,
        tenant=current_tenant
    ).order_by('-changed_at')
    
    context = {
        'booking': booking,
        'history': history,
        'tenant': current_tenant,
        'can_cancel': (
            booking.status in ['confirmed', 'pending'] and
            booking.event.start_date > timezone.now()
        ),
    }
    
    return render(request, 'bookings/booking_detail.html', context)


@login_required
def booking_create(request, event_id):
    """Create a new booking for an event"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    event = get_object_or_404(Event, id=event_id, tenant=current_tenant)
    
    # Check if user can book this event
    if not event.is_active:
        messages.error(request, 'This event is not active.')
        return redirect('events:event_detail', event_id=event.id)
    
    if event.start_date <= timezone.now():
        messages.error(request, 'This event has already started or ended.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Check if user already has a booking
    existing_booking = Booking.objects.filter(
        event=event,
        user=request.user,
        tenant=current_tenant,
        status__in=['confirmed', 'pending']
    ).exists()
    
    if existing_booking:
        messages.warning(request, 'You already have a booking for this event.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Check capacity
    booking_count = Booking.objects.filter(
        event=event,
        status='confirmed',
        tenant=current_tenant
    ).count()
    
    if booking_count >= event.capacity:
        messages.error(request, 'This event is fully booked.')
        return redirect('events:event_detail', event_id=event.id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, event=event, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.event = event
            booking.user = request.user
            booking.tenant = current_tenant
            booking.confirmation_code = str(uuid.uuid4())[:8].upper()
            booking.status = 'confirmed'  # Auto-confirm for now
            booking.save()
            
            # Create booking history entry
            BookingHistory.objects.create(
                booking=booking,
                new_status='confirmed',
                reason='Booking created and confirmed',
                tenant=current_tenant
            )
            
            messages.success(
                request,
                f'Successfully booked "{event.title}"! Your confirmation code is: {booking.confirmation_code}'
            )
            return redirect('bookings:booking_detail', booking_id=booking.id)
    else:
        form = BookingForm(event=event, user=request.user)
    
    context = {
        'form': form,
        'event': event,
        'tenant': current_tenant,
        'available_spots': event.capacity - booking_count,
    }
    
    return render(request, 'bookings/booking_form.html', context)


@login_required
def booking_cancel(request, booking_id):
    """Cancel a booking"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        tenant=current_tenant
    )
    
    # Check if booking can be cancelled
    if booking.status == 'cancelled':
        messages.warning(request, 'This booking is already cancelled.')
        return redirect('bookings:booking_detail', booking_id=booking.id)
    
    if booking.event.start_date <= timezone.now():
        messages.error(request, 'Cannot cancel booking for an event that has already started.')
        return redirect('bookings:booking_detail', booking_id=booking.id)
    
    if request.method == 'POST':
        old_status = booking.status
        booking.status = 'cancelled'
        booking.save()
        
        # Create booking history entry
        BookingHistory.objects.create(
            booking=booking,
            old_status=old_status,
            new_status='cancelled',
            reason=f'Booking cancelled by user. Previous status: {old_status}',
            tenant=current_tenant
        )
        
        messages.success(request, f'Booking for "{booking.event.title}" has been cancelled.')
        return redirect('bookings:booking_list')
    
    context = {
        'booking': booking,
        'tenant': current_tenant,
    }
    
    return render(request, 'bookings/booking_confirm_cancel.html', context)


@login_required
def booking_update(request, booking_id):
    """Update booking status (admin only)"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    # Check if user can update bookings
    if not request.user.is_organizer():
        messages.error(request, 'You do not have permission to update bookings.')
        return redirect('bookings:booking_list')
    
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        tenant=current_tenant
    )
    
    if request.method == 'POST':
        form = BookingUpdateForm(request.POST, instance=booking)
        if form.is_valid():
            old_status = booking.status
            booking = form.save()
            
            # Create booking history entry if status changed
            if old_status != booking.status:
                BookingHistory.objects.create(
                    booking=booking,
                    old_status=old_status,
                    new_status=booking.status,
                    reason=f'Status changed from {old_status} to {booking.status} by {request.user.email}',
                    tenant=current_tenant
                )
            
            messages.success(request, f'Booking updated successfully.')
            return redirect('bookings:booking_detail', booking_id=booking.id)
    else:
        form = BookingUpdateForm(instance=booking)
    
    context = {
        'form': form,
        'booking': booking,
        'tenant': current_tenant,
    }
    
    return render(request, 'bookings/booking_update_form.html', context)


@login_required
def admin_booking_list(request):
    """List all bookings for admin (organizer only)"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:dashboard')
    
    # Check if user can view all bookings
    if not request.user.is_organizer():
        messages.error(request, 'You do not have permission to view all bookings.')
        return redirect('bookings:booking_list')
    
    # Get search form
    search_form = BookingSearchForm(request.GET)
    bookings = Booking.objects.filter(
        tenant=current_tenant
    ).select_related('event', 'event__event_type', 'user')
    
    # Apply search filters
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        status = search_form.cleaned_data.get('status')
        date_from = search_form.cleaned_data.get('date_from')
        date_to = search_form.cleaned_data.get('date_to')
        
        if search_query:
            bookings = bookings.filter(
                Q(event__title__icontains=search_query) |
                Q(user__email__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query)
            )
        
        if status and status != 'all':
            bookings = bookings.filter(status=status)
        
        if date_from:
            bookings = bookings.filter(event__start_date__date__gte=date_from)
        
        if date_to:
            bookings = bookings.filter(event__start_date__date__lte=date_to)
    
    # Order by booking date (newest first)
    bookings = bookings.order_by('-booking_date')
    
    # Pagination
    paginator = Paginator(bookings, 20)  # 20 bookings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'bookings': page_obj,
        'search_form': search_form,
        'tenant': current_tenant,
        'total_bookings': bookings.count(),
        'is_admin_view': True,
    }
    
    return render(request, 'bookings/admin_booking_list.html', context)


# API Endpoints for AJAX requests
@login_required
@require_http_methods(["GET"])
def booking_stats_api(request):
    """API endpoint to get booking statistics"""
    current_tenant = get_current_tenant()
    if not current_tenant:
        return JsonResponse({'error': 'No tenant context found'}, status=400)
    
    # Check if user can view stats
    if not request.user.is_organizer():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        total_bookings = Booking.objects.filter(tenant=current_tenant).count()
        confirmed_bookings = Booking.objects.filter(
            tenant=current_tenant,
            status='confirmed'
        ).count()
        pending_bookings = Booking.objects.filter(
            tenant=current_tenant,
            status='pending'
        ).count()
        cancelled_bookings = Booking.objects.filter(
            tenant=current_tenant,
            status='cancelled'
        ).count()
        
        # Get bookings by event
        event_bookings = Booking.objects.filter(
            tenant=current_tenant,
            status='confirmed'
        ).values('event__title').annotate(
            booking_count=Count('id')
        ).order_by('-booking_count')[:10]
        
        return JsonResponse({
            'success': True,
            'stats': {
                'total_bookings': total_bookings,
                'confirmed_bookings': confirmed_bookings,
                'pending_bookings': pending_bookings,
                'cancelled_bookings': cancelled_bookings,
                'event_bookings': list(event_bookings)
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
