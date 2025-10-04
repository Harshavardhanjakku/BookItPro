from django.http import Http404
from django.shortcuts import get_object_or_404
from accounts.models import Tenant
from .multitenant import set_current_tenant, clear_current_tenant
import re


class TenantMiddleware:
    """Middleware to detect and set the current tenant"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Clear any existing tenant
        clear_current_tenant()
        
        # Extract tenant from URL or subdomain
        tenant = self.get_tenant_from_request(request)
        
        if tenant:
            set_current_tenant(tenant)
            request.tenant = tenant
        else:
            request.tenant = None
        
        response = self.get_response(request)
        
        # Clear tenant after request
        clear_current_tenant()
        
        return response
    
    def get_tenant_from_request(self, request):
        """Extract tenant from request URL or subdomain"""
        host = request.get_host()
        path = request.path
        
        # Method 1: Subdomain-based (e.g., techcorp.localhost:8000)
        if '.' in host and not host.startswith('127.0.0.1') and not host.startswith('localhost'):
            subdomain = host.split('.')[0]
            try:
                return Tenant.objects.get(slug=subdomain, is_active=True)
            except Tenant.DoesNotExist:
                pass
        
        # Method 2: URL-based (e.g., /techcorp-events/events/)
        path_match = re.match(r'^/([^/]+)/', path)
        if path_match:
            tenant_slug = path_match.group(1)
            try:
                return Tenant.objects.get(slug=tenant_slug, is_active=True)
            except Tenant.DoesNotExist:
                pass
        
        # Method 3: Session-based (for logged-in users)
        if hasattr(request, 'user') and request.user.is_authenticated:
            if hasattr(request.user, 'tenant') and request.user.tenant:
                return request.user.tenant
        
        return None
