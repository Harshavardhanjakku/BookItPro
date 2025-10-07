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
    
    # User Management URLs (Admin only)
    path('users/', views.user_management, name='user_management'),
    path('users/add/', views.add_user_to_organization, name='add_user'),
    path('users/<int:user_id>/update-role/', views.update_user_role, name='update_user_role'),
    path('users/<int:user_id>/remove/', views.remove_user_from_organization, name='remove_user'),
    
    # Password Reset URLs
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # API endpoints for schema management
    path('api/create-schema/', views.create_tenant_schema_api, name='create_tenant_schema_api'),
    path('api/list-tenants/', views.list_tenants_api, name='list_tenants_api'),
]
