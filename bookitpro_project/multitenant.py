from django.db import models
from django.conf import settings
import threading

# Thread-local storage for tenant
_thread_locals = threading.local()

def set_current_tenant(tenant):
    """Set the current tenant for this thread"""
    _thread_locals.tenant = tenant

def get_current_tenant():
    """Get the current tenant for this thread"""
    return getattr(_thread_locals, 'tenant', None)

def clear_current_tenant():
    """Clear the current tenant for this thread"""
    if hasattr(_thread_locals, 'tenant'):
        delattr(_thread_locals, 'tenant')


class TenantAwareModel(models.Model):
    """Abstract base model for tenant-aware models"""
    tenant_schema = models.CharField(max_length=100, blank=True)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        current_tenant = get_current_tenant()
        if current_tenant:
            self.tenant_schema = current_tenant.slug
        super().save(*args, **kwargs)


class TenantRouter:
    """Database router for tenant-based schema routing"""
    
    def db_for_read(self, model, **hints):
        """Point all read operations to the correct schema"""
        return 'default'
    
    def db_for_write(self, model, **hints):
        """Point all write operations to the correct schema"""
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations between objects in the same schema"""
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow migrations only for the default database"""
        return db == 'default'
