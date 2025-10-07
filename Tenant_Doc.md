I'll provide you with a comprehensive explanation of the multi-tenant architecture in your BookItPro project, including all endpoints, file locations, and code snippets. Let me analyze the codebase first.


[5 tools called]

Now let me read the URLs and forms to understand the complete structure:


[5 tools called]

Now let me check the main project URLs to understand the complete routing:


[1 tool called]

Perfect! Now I have a complete understanding of the multi-tenant architecture. Let me provide you with a comprehensive explanation.

# **BookItPro Multi-Tenant Architecture - Complete Explanation**

## **🏗️ Architecture Overview**

Your BookItPro project implements a **PostgreSQL Schema-based Multi-Tenancy** architecture where:
- Each tenant (organization) gets its own PostgreSQL schema
- All tenant data is isolated in separate schemas
- Users belong to specific tenants with role-based access
- Middleware automatically detects and routes requests to the correct tenant

---

## **📁 Core Multi-Tenant Files & Components**

### **1. Multi-Tenant Core (`bookitpro_project/multitenant.py`)**

```python
# Thread-local storage for tenant context
_thread_locals = threading.local()

def set_current_tenant(tenant):
    """Set the current tenant for this thread"""
    _thread_locals.tenant = tenant

def get_current_tenant():
    """Get the current tenant for this thread"""
    return getattr(_thread_locals, 'tenant', None)

class TenantAwareModel(models.Model):
    """Abstract base model for tenant-aware models"""
    tenant_schema = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        current_tenant = get_current_tenant()
        if current_tenant:
            self.tenant_schema = current_tenant.slug
            if hasattr(self, 'tenant'):
                self.tenant = current_tenant
        super().save(*args, **kwargs)
```

**Purpose**: 
- Manages tenant context using thread-local storage
- Provides base model for all tenant-aware models
- Automatically sets tenant information when saving models

---

### **2. Tenant Middleware (`bookitpro_project/tenant_middleware.py`)**

```python
class TenantMiddleware:
    def __call__(self, request):
        clear_current_tenant()
        tenant = self.get_tenant_from_request(request)
        
        if tenant:
            set_current_tenant(tenant)
            request.tenant = tenant
        
        response = self.get_response(request)
        clear_current_tenant()
        return response
    
    def get_tenant_from_request(self, request):
        # Method 1: Subdomain-based (techcorp.localhost:8000)
        # Method 2: URL-based (/techcorp-events/events/)
        # Method 3: Session-based (for logged-in users)
```

**Purpose**: 
- Automatically detects tenant from URL/subdomain/session
- Sets tenant context for the entire request
- Supports multiple tenant detection methods

---

### **3. Tenant Model (`accounts/models.py`)**

```python
class Tenant(models.Model):
    """Organization/Tenant model for multitenant architecture"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="URL-friendly name")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    ROLE_CHOICES = [
        ('admin', 'Organizer Admin'),
        ('manager', 'Event Manager'),
        ('attendee', 'Attendee'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attendee')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
```

**Purpose**: 
- Defines tenant/organization structure
- Custom user model with role-based permissions
- Links users to specific tenants

---

## **🔗 API Endpoints & URL Structure**

### **Main Project URLs (`bookitpro_project/urls.py`)**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),           # Authentication & tenant management
    path('events/', include('events.urls')),      # Event management
    path('bookings/', include('bookings.urls')), # Booking management
]
```

### **Account Management URLs (`accounts/urls.py`)**

#### **Authentication Endpoints:**
- `GET/POST /` - Home page (shows available tenants)
- `GET/POST /login/` - User login
- `GET /logout/` - User logout
- `GET/POST /register/` - Individual user registration
- `GET/POST /register-tenant/` - Organization registration

#### **Dashboard & Profile:**
- `GET /dashboard/` - User dashboard (role-based)
- `GET/POST /profile/` - User profile management

#### **User Management (Admin Only):**
- `GET /users/` - List organization users
- `GET/POST /users/add/` - Add user to organization
- `GET/POST /users/<id>/update-role/` - Update user role
- `GET/POST /users/<id>/remove/` - Remove user from organization

#### **Password Reset:**
- `GET/POST /password-reset/` - Request password reset
- `GET /password-reset/done/` - Password reset email sent
- `GET/POST /reset/<uidb64>/<token>/` - Reset password form
- `GET /reset/done/` - Password reset complete

#### **API Endpoints:**
- `POST /api/create-schema/` - Create tenant schema
- `GET /api/list-tenants/` - List all tenants

---

## **🏢 Tenant Creation Process**

### **1. Individual User Registration (`accounts/views.py`)**

```python
class UserRegistrationView(CreateView):
    def form_valid(self, form):
        # Create the user first
        response = super().form_valid(form)
        user = self.object
        
        # Create a personal tenant for the user
        tenant_name = f"{user.first_name} {user.last_name}'s Events"
        tenant_slug = f"{user.first_name.lower()}-{user.last_name.lower()}-events"
        
        tenant = Tenant.objects.create(
            name=tenant_name,
            slug=tenant_slug,
            description=f"Personal event space for {user.first_name} {user.last_name}",
            is_active=True
        )
        
        # Assign tenant to user
        user.tenant = tenant
        user.save()
        
        # Create schema for the tenant
        schema_name = f"tenant_{tenant.slug}"
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
            create_tenant_tables(cursor, schema_name)
```

**Endpoint**: `POST /register/`
**Purpose**: Creates individual users with personal tenant spaces

### **2. Organization Registration (`accounts/views.py`)**

```python
class TenantRegistrationView(CreateView):
    def form_valid(self, form):
        # Create the tenant first
        response = super().form_valid(form)
        tenant = self.object
        
        # Create admin user for the tenant
        admin_user = User.objects.create_user(
            email=admin_data['organizer_email'],
            first_name=admin_data['organizer_first_name'],
            last_name=admin_data['organizer_last_name'],
            password=admin_data['organizer_password'],
            role='admin',
            tenant=tenant
        )
        
        # Create schema for the tenant
        schema_name = f"tenant_{tenant.slug}"
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
            create_tenant_tables(cursor, schema_name)
```

**Endpoint**: `POST /register-tenant/`
**Purpose**: Creates organizations with admin users

---

## **🗄️ Schema Creation Process**

### **Schema Creation Function (`accounts/views.py`)**

```python
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
    
    # Bookings table
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
```

**Purpose**: Creates isolated database tables for each tenant

### **Management Command (`accounts/management/commands/create_tenant_schemas.py`)**

```python
class Command(BaseCommand):
    help = 'Create PostgreSQL schemas for all tenants'
    
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            tenants = Tenant.objects.all()
            
            for tenant in tenants:
                schema_name = f"tenant_{tenant.slug}"
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
                self.create_tenant_tables(cursor, schema_name)
```

**Command**: `python manage.py create_tenant_schemas`
**Purpose**: Bulk create schemas for existing tenants

---

## **👥 Role Assignment & User Management**

### **Role-Based Access Control**

#### **User Roles (`accounts/models.py`)**
```python
ROLE_CHOICES = [
    ('admin', 'Organizer Admin'),      # Full organization control
    ('manager', 'Event Manager'),      # Event management only
    ('attendee', 'Attendee'),         # Booking events only
]

def is_organizer(self):
    return self.role in ['admin', 'manager']

def is_admin(self):
    return self.role == 'admin'

def is_manager(self):
    return self.role == 'manager'
```

#### **Role Assignment Endpoints:**

**1. Add User to Organization (`accounts/views.py`)**
```python
@login_required
def add_user_to_organization(request):
    # Check if user is admin
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to add users.')
        return redirect('accounts:user_management')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        # Check if user already exists
        try:
            user = User.objects.get(email=email)
            user.tenant = current_tenant
            user.role = role
            user.save()
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create_user(
                email=email,
                role=role,
                tenant=current_tenant,
                password='temp123'
            )
```

**Endpoint**: `POST /users/add/`
**Access**: Admin only

**2. Update User Role (`accounts/views.py`)**
```python
@login_required
def update_user_role(request, user_id):
    # Check if user is admin
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to update user roles.')
        return redirect('accounts:user_management')
    
    user = get_object_or_404(User, id=user_id, tenant=current_tenant)
    
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in ['admin', 'manager', 'attendee']:
            user.role = new_role
            user.save()
```

**Endpoint**: `POST /users/<id>/update-role/`
**Access**: Admin only

**3. Remove User from Organization (`accounts/views.py`)**
```python
@login_required
def remove_user_from_organization(request, user_id):
    # Check if user is admin
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to remove users.')
        return redirect('accounts:user_management')
    
    user = get_object_or_404(User, id=user_id, tenant=current_tenant)
    
    # Prevent admin from removing themselves
    if user == request.user:
        messages.error(request, 'You cannot remove yourself from the organization.')
        return redirect('accounts:user_management')
    
    if request.method == 'POST':
        user.tenant = None
        user.role = 'attendee'  # Reset to default role
        user.save()
```

**Endpoint**: `POST /users/<id>/remove/`
**Access**: Admin only

---

## **🎯 Tenant-Aware Models**

### **Event Model (`events/models.py`)**
```python
class Event(TenantAwareModel):
    """Event model for the booking system"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    
    # Event details
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
```

### **Booking Model (`bookings/models.py`)**
```python
class Booking(TenantAwareModel):
    """Booking model for event reservations"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    tenant = models.ForeignKey('accounts.Tenant', on_delete=models.CASCADE, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(default=timezone.now)
    confirmation_code = models.CharField(max_length=20, unique=True, blank=True)
```

**Key Features**:
- All models inherit from `TenantAwareModel`
- Automatic tenant assignment on save
- Tenant isolation through schema separation
- Foreign key relationships maintained across schemas

---

## **🔧 Configuration Files**

### **Settings (`bookitpro_project/settings.py`)**
```python
# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Database routing for multitenancy
DATABASE_ROUTERS = ['bookitpro_project.multitenant.TenantRouter']

# Middleware includes tenant middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'bookitpro_project.tenant_middleware.TenantMiddleware',  # Tenant middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# PostgreSQL database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bookitpro',
        'USER': 'postgres',
        'PASSWORD': 'CanvasHarsha123',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=public'
        }
    }
}
```

---

## **📊 Complete Flow Summary**

### **1. Tenant Creation Flow:**
1. **Individual Registration** → Creates user + personal tenant + schema
2. **Organization Registration** → Creates tenant + admin user + schema
3. **Schema Creation** → PostgreSQL schema with isolated tables

### **2. User Management Flow:**
1. **Admin Login** → Detects tenant context
2. **Add Users** → Assign users to organization with roles
3. **Role Management** → Update/remove user roles
4. **Tenant Isolation** → All operations scoped to tenant

### **3. Data Isolation:**
1. **Middleware Detection** → Identifies tenant from request
2. **Context Setting** → Sets tenant in thread-local storage
3. **Model Saving** → Automatic tenant assignment
4. **Schema Routing** → Data stored in tenant-specific schema

This architecture provides complete tenant isolation while maintaining a single Django application instance, making it highly scalable and maintainable.