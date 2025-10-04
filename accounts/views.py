from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection
from .models import Tenant
from .forms import UserRegistrationForm, UserLoginForm, TenantRegistrationForm
from bookitpro_project.multitenant import set_current_tenant

User = get_user_model()


def home(request):
    """Home page showing available tenants"""
    tenants = Tenant.objects.filter(is_active=True)
    return render(request, 'accounts/home.html', {'tenants': tenants})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                # Set tenant context if user has a tenant
                if user.tenant:
                    set_current_tenant(user.tenant)
                messages.success(request, f'Welcome back, {user.first_name or user.email}!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:home')


class UserRegistrationView(CreateView):
    """User registration view - creates user with personal tenant and schema"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        # Create the user first
        response = super().form_valid(form)
        user = self.object
        
        # Create a personal tenant for the user
        tenant_name = f"{user.first_name} {user.last_name}'s Events"
        tenant_slug = f"{user.first_name.lower()}-{user.last_name.lower()}-events"
        
        # Ensure slug is unique
        counter = 1
        original_slug = tenant_slug
        while Tenant.objects.filter(slug=tenant_slug).exists():
            tenant_slug = f"{original_slug}-{counter}"
            counter += 1
        
        tenant = Tenant.objects.create(
            name=tenant_name,
            slug=tenant_slug,
            description=f"Personal event space for {user.first_name} {user.last_name}",
            is_active=True
        )
        
        # Assign tenant to user
        user.tenant = tenant
        user.role = 'admin'  # Make them admin of their personal tenant
        user.save()
        
        # Create schema for the tenant
        try:
            schema_name = f"tenant_{tenant.slug}"
            with connection.cursor() as cursor:
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
                create_tenant_tables(cursor, schema_name)
            
            messages.success(self.request, f'Account and personal event space created successfully! Your tenant: {tenant_name}')
        except Exception as e:
            messages.warning(self.request, f'Account created but schema creation failed: {str(e)}')
        
        return response


class TenantRegistrationView(CreateView):
    """Tenant registration view for organizers - creates tenant, admin user, and schema"""
    model = Tenant
    form_class = TenantRegistrationForm
    template_name = 'accounts/register_tenant.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        # Create the tenant first
        response = super().form_valid(form)
        tenant = self.object
        
        # Create admin user for the tenant
        admin_data = form.cleaned_data
        admin_user = User.objects.create_user(
            email=admin_data['organizer_email'],
            first_name=admin_data['organizer_first_name'],
            last_name=admin_data['organizer_last_name'],
            password=admin_data['organizer_password'],
            role='admin',
            tenant=tenant
        )
        
        # Create schema for the tenant
        try:
            schema_name = f"tenant_{tenant.slug}"
            with connection.cursor() as cursor:
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
                create_tenant_tables(cursor, schema_name)
            
            messages.success(self.request, f'Organization "{tenant.name}" registered successfully! Admin user created. Schema: {schema_name}')
        except Exception as e:
            messages.warning(self.request, f'Organization created but schema creation failed: {str(e)}')
        
        return response


@login_required
def dashboard(request):
    """User dashboard with real data"""
    user = request.user
    tenant = getattr(request, 'tenant', None)
    
    if not tenant:
        messages.error(request, 'No tenant context found.')
        return redirect('accounts:home')
    
    context = {
        'user': user,
        'tenant': tenant,
        'events': [],
        'bookings': [],
        'event_count': 0,
        'booking_count': 0,
    }
    
    if user.is_organizer():
        # Show organizer dashboard with real data
        from events.models import Event, EventType
        from bookings.models import Booking
        
        # Get events for this tenant
        events = Event.objects.filter(tenant_schema=tenant.slug).order_by('-created_at')[:5]
        event_count = Event.objects.filter(tenant_schema=tenant.slug).count()
        
        # Get bookings for this tenant
        bookings = Booking.objects.filter(tenant_schema=tenant.slug).order_by('-booking_date')[:5]
        booking_count = Booking.objects.filter(tenant_schema=tenant.slug).count()
        
        # Get event types
        event_types = EventType.objects.filter(tenant_schema=tenant.slug).count()
        
        context.update({
            'dashboard_type': 'organizer',
            'message': f'Welcome to your organizer dashboard for {tenant.name}!',
            'events': events,
            'bookings': bookings,
            'event_count': event_count,
            'booking_count': booking_count,
            'event_types_count': event_types,
            'next_steps': [
                'Create your first event',
                'Set up event types',
                'Manage bookings',
                'View analytics'
            ]
        })
    else:
        # Show attendee dashboard with real data
        from events.models import Event
        from bookings.models import Booking
        
        # Get user's bookings
        bookings = Booking.objects.filter(
            user=user,
            tenant_schema=tenant.slug
        ).order_by('-booking_date')[:5]
        booking_count = Booking.objects.filter(
            user=user,
            tenant_schema=tenant.slug
        ).count()
        
        # Get upcoming events
        from django.utils import timezone
        events = Event.objects.filter(
            tenant_schema=tenant.slug,
            is_active=True,
            start_date__gt=timezone.now()
        ).order_by('start_date')[:5]
        event_count = Event.objects.filter(
            tenant_schema=tenant.slug,
            is_active=True,
            start_date__gt=timezone.now()
        ).count()
        
        context.update({
            'dashboard_type': 'attendee',
            'message': f'Welcome {user.first_name}! Browse and book events.',
            'events': events,
            'bookings': bookings,
            'event_count': event_count,
            'booking_count': booking_count,
            'next_steps': [
                'Browse available events',
                'Book your first event',
                'View your bookings',
                'Update your profile'
            ]
        })
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        # Handle profile updates
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html', {'user': request.user})


# Password reset views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


# API Endpoints for Schema Management
@csrf_exempt
@require_http_methods(["POST"])
def create_tenant_schema_api(request):
    """API endpoint to create schema for a specific tenant"""
    try:
        data = request.POST if request.method == 'POST' else {}
        tenant_slug = data.get('tenant_slug')
        
        if not tenant_slug:
            return JsonResponse({
                'success': False,
                'error': 'tenant_slug parameter is required'
            }, status=400)
        
        # Check if tenant exists
        try:
            tenant = Tenant.objects.get(slug=tenant_slug)
        except Tenant.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Tenant with slug "{tenant_slug}" does not exist'
            }, status=404)
        
        # Create schema
        schema_name = f"tenant_{tenant.slug}"
        
        with connection.cursor() as cursor:
            # Create schema if it doesn't exist
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
            
            # Create tables in the tenant schema
            create_tenant_tables(cursor, schema_name)
        
        return JsonResponse({
            'success': True,
            'message': f'Successfully created schema: {schema_name}',
            'schema_name': schema_name,
            'tenant_name': tenant.name
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def list_tenants_api(request):
    """API endpoint to list all tenants"""
    try:
        tenants = Tenant.objects.filter(is_active=True)
        tenant_list = []
        
        for tenant in tenants:
            tenant_list.append({
                'id': tenant.id,
                'name': tenant.name,
                'slug': tenant.slug,
                'description': tenant.description,
                'schema_name': f"tenant_{tenant.slug}",
                'created_at': tenant.created_at.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'tenants': tenant_list,
            'count': len(tenant_list)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def create_tenant_tables(cursor, schema_name):
    """Create necessary tables in tenant schema"""
    
    # Events table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS "{schema_name}".events_eventtype (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            description TEXT,
            icon VARCHAR(50),
            tenant_schema VARCHAR(100),
            CONSTRAINT unique_name_per_tenant UNIQUE (name, tenant_schema)
        )
    """)
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS "{schema_name}".events_event (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT NOT NULL,
            event_type_id INTEGER REFERENCES "{schema_name}".events_eventtype(id),
            tenant_id INTEGER REFERENCES public.accounts_tenant(id),
            start_date TIMESTAMP WITH TIME ZONE NOT NULL,
            end_date TIMESTAMP WITH TIME ZONE NOT NULL,
            location VARCHAR(200) NOT NULL,
            capacity INTEGER NOT NULL,
            price DECIMAL(10,2) DEFAULT 0.00,
            image VARCHAR(100),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            tenant_schema VARCHAR(100)
        )
    """)
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS "{schema_name}".bookings_booking (
            id SERIAL PRIMARY KEY,
            event_id INTEGER REFERENCES "{schema_name}".events_event(id),
            user_id INTEGER REFERENCES public.accounts_user(id),
            booking_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            status VARCHAR(20) DEFAULT 'confirmed',
            notes TEXT,
            tenant_schema VARCHAR(100),
            CONSTRAINT unique_booking_per_user_event UNIQUE (event_id, user_id, tenant_schema)
        )
    """)
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS "{schema_name}".bookings_bookinghistory (
            id SERIAL PRIMARY KEY,
            booking_id INTEGER REFERENCES "{schema_name}".bookings_booking(id),
            action VARCHAR(50) NOT NULL,
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            notes TEXT,
            tenant_schema VARCHAR(100)
        )
    """)
