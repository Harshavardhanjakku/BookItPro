from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
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
    """User registration view"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response


class TenantRegistrationView(CreateView):
    """Tenant registration view for organizers"""
    model = Tenant
    form_class = TenantRegistrationForm
    template_name = 'accounts/register_tenant.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Organization registered successfully! Please log in.')
        return response


@login_required
def dashboard(request):
    """User dashboard"""
    user = request.user
    context = {
        'user': user,
        'tenant': getattr(request, 'tenant', None),
    }
    
    if user.is_organizer():
        # Show organizer dashboard
        context['events'] = user.tenant.events.all() if user.tenant else []
        return render(request, 'accounts/organizer_dashboard.html', context)
    else:
        # Show attendee dashboard
        context['bookings'] = user.bookings.all()
        return render(request, 'accounts/attendee_dashboard.html', context)


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
