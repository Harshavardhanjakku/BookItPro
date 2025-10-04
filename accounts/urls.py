from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('register-tenant/', views.TenantRegistrationView.as_view(), name='register_tenant'),
    
    # Dashboard and Profile URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Password Reset URLs
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
