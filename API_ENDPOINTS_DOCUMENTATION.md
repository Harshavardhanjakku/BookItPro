# 📚 BookItPro - Complete API Endpoints Documentation

## 🏠 **Base URL**: `http://127.0.0.1:8000`

## 🎉 **CURRENT STATUS: FULLY FUNCTIONAL MULTITENANT SYSTEM**

### ✅ **WORKING FEATURES:**
- **User Registration** → Creates user + personal tenant + schema automatically
- **Tenant Registration** → Creates organization + admin user + schema automatically  
- **Authentication System** → Complete login/logout with password validation disabled
- **Dashboard System** → Role-based dashboards (organizer/attendee) with proper context
- **API Endpoints** → Schema management and tenant listing
- **Multitenant Isolation** → Schema-based separation in PostgreSQL
- **Auto Schema Creation** → All registrations create schemas automatically

### 🔄 **NEXT TO IMPLEMENT:**
- **Event Management** → CRUD operations for events
- **Booking System** → Event booking functionality
- **Enhanced Permissions** → More granular role-based access

---

## 🔐 **AUTHENTICATION ENDPOINTS** (`/accounts/`)

### **1. Home Page**
- **URL**: `GET /`
- **Purpose**: Display available tenants/organizations
- **Parameters**: None
- **Response**: HTML page with list of active tenants
- **Functionality**: Shows all active organizations that users can join

### **2. User Login**
- **URL**: `POST /login/`
- **Purpose**: Authenticate existing users
- **Parameters**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**: Redirects to dashboard on success
- **Functionality**: Logs in user and sets tenant context

### **3. User Logout**
- **URL**: `GET /logout/`
- **Purpose**: Log out current user
- **Parameters**: None
- **Response**: Redirects to home page
- **Functionality**: Clears user session and tenant context

### **4. User Registration** ⭐ **UPDATED - NOW CREATES SCHEMA AUTOMATICALLY**
- **URL**: `POST /register/`
- **Purpose**: Register new individual users with personal tenant
- **Parameters**:
  ```json
  {
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password1": "admin",
    "password2": "admin",
    "phone": "+1234567890",
    "role": "attendee"
  }
  ```
- **Response**: Redirects to login page with success message
- **Functionality**: 
  - ✅ Creates user account
  - ✅ Creates personal tenant: "John Doe's Events"
  - ✅ Creates schema: `tenant_john-doe-events`
  - ✅ Makes user admin of their personal tenant
  - ✅ Creates all necessary tables in schema

### **5. Tenant Registration** ⭐ **UPDATED - NOW CREATES SCHEMA AUTOMATICALLY**
- **URL**: `POST /register-tenant/`
- **Purpose**: Register new organization/tenant with admin user
- **Parameters**:
  ```json
  {
    "name": "My Company",
    "slug": "my-company",
    "description": "Event management company",
    "organizer_email": "admin@mycompany.com",
    "organizer_first_name": "Jane",
    "organizer_last_name": "Smith",
    "organizer_password": "admin"
  }
  ```
- **Response**: Redirects to login page with success message
- **Functionality**:
  - ✅ Creates organization/tenant
  - ✅ Creates admin user for organization
  - ✅ Creates schema: `tenant_my-company`
  - ✅ Creates all necessary tables in schema

### **6. Dashboard** ⭐ **FIXED - NO MORE ERRORS**
- **URL**: `GET /dashboard/`
- **Purpose**: User dashboard after login
- **Parameters**: None (requires authentication)
- **Response**: HTML dashboard page
- **Functionality**: 
  - ✅ Shows user information and role
  - ✅ Displays tenant/organization information
  - ✅ Shows next steps for development
  - ✅ Role-based dashboard (organizer vs attendee)
  - ✅ No more AttributeError for tenant.events

### **7. Profile**
- **URL**: `GET /profile/`
- **Purpose**: View/edit user profile
- **Parameters**: None (requires authentication)
- **Response**: HTML profile page
- **Functionality**: Display and edit user information

---

## 🔄 **PASSWORD RESET ENDPOINTS**

### **8. Password Reset Request**
- **URL**: `POST /password-reset/`
- **Purpose**: Request password reset email
- **Parameters**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response**: Confirmation page
- **Functionality**: Sends password reset email

### **9. Password Reset Done**
- **URL**: `GET /password-reset/done/`
- **Purpose**: Confirmation page after reset request
- **Parameters**: None
- **Response**: HTML confirmation page

### **10. Password Reset Confirm**
- **URL**: `GET /reset/<uidb64>/<token>/`
- **Purpose**: Reset password with token
- **Parameters**: URL parameters (uidb64, token)
- **Response**: Password reset form
- **Functionality**: Allows user to set new password

### **11. Password Reset Complete**
- **URL**: `GET /reset/done/`
- **Purpose**: Confirmation after successful reset
- **Parameters**: None
- **Response**: HTML success page

---

## 🏢 **TENANT/SCHEMA MANAGEMENT API**

### **12. List All Tenants**
- **URL**: `GET /api/list-tenants/`
- **Purpose**: Get all active tenants
- **Parameters**: None
- **Response**:
  ```json
  {
    "success": true,
    "tenants": [
      {
        "id": 1,
        "name": "TechCorp Events",
        "slug": "techcorp-events",
        "description": "Technology events",
        "schema_name": "tenant_techcorp-events",
        "created_at": "2024-01-15T10:30:00Z"
      }
    ],
    "count": 1
  }
  ```
- **Functionality**: Returns all active tenants with schema names

### **13. Create Tenant Schema**
- **URL**: `POST /api/create-schema/`
- **Purpose**: Create database schema for specific tenant
- **Parameters**:
  ```json
  {
    "tenant_slug": "techcorp-events"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Successfully created schema: tenant_techcorp-events",
    "schema_name": "tenant_techcorp-events",
    "tenant_name": "TechCorp Events"
  }
  ```
- **Functionality**: Creates PostgreSQL schema and tables for tenant

---

## 🎉 **EVENTS ENDPOINTS** (`/events/`)

### **14. Event List**
- **URL**: `GET /events/`
- **Purpose**: List all events (placeholder)
- **Parameters**: None
- **Response**: HTML page (currently placeholder)
- **Functionality**: Will show events for current tenant

---

## 📅 **BOOKINGS ENDPOINTS** (`/bookings/`)

### **15. Booking List**
- **URL**: `GET /bookings/`
- **Purpose**: List user bookings (placeholder)
- **Parameters**: None
- **Response**: HTML page (currently placeholder)
- **Functionality**: Will show user's bookings

---

## ⚙️ **ADMIN ENDPOINTS**

### **16. Django Admin**
- **URL**: `GET /admin/`
- **Purpose**: Django admin interface
- **Parameters**: None
- **Response**: Admin login page
- **Functionality**: Manage users, tenants, events, bookings

---

## 🔧 **MANAGEMENT COMMANDS**

### **17. Create All Tenant Schemas**
- **Command**: `python manage.py create_tenant_schemas`
- **Purpose**: Create schemas for all existing tenants
- **Parameters**: None
- **Functionality**: Bulk create all missing tenant schemas

---

## ✅ **CURRENT SYSTEM STATUS - ALL ISSUES FIXED!**

### **✅ RESOLVED ISSUES:**
1. **User Registration** (`/register/`) → ✅ Now creates user + personal tenant + schema automatically
2. **Tenant Registration** (`/register-tenant/`) → ✅ Now creates tenant + admin user + schema automatically
3. **Dashboard Errors** → ✅ Fixed AttributeError for tenant.events
4. **Schema Creation** → ✅ Automatic for all registrations

### **✅ CURRENT WORKING FEATURES:**
1. **User Registration** → ✅ Creates user + personal tenant + schema + admin role
2. **Tenant Registration** → ✅ Creates tenant + admin user + schema + all tables
3. **Authentication System** → ✅ Complete with password validation disabled for development
4. **Dashboard System** → ✅ Role-based dashboards with proper context
5. **API Endpoints** → ✅ Schema management and tenant listing
6. **Multitenant Isolation** → ✅ Proper schema-based separation

---

## 🎯 **NEXT STEPS TO IMPLEMENT:**

1. **Event Management System** → CRUD operations for events
2. **Booking System** → Event booking functionality  
3. **Enhanced Role-Based Access** → More granular permissions
4. **Event Types Management** → Categories and types
5. **Analytics Dashboard** → Statistics and reports

---

## 📊 **USER ROLES & PERMISSIONS:**

### **👑 Organizer Admin**
- Manage all events and bookings
- Access to all tenant data
- Can create/edit/delete events

### **👨‍💼 Event Manager**
- Manage only events
- Cannot access booking management
- Can create/edit events

### **👤 Attendee/User**
- Browse and book events
- View own bookings
- Cannot create events

---

## 🔄 **COMPLETE WORKFLOW - NOW FULLY FUNCTIONAL:**

### **For New Organization:**
1. **Register Tenant** → `/register-tenant/` ✅ **Creates tenant + admin user + schema automatically**
2. **Login as Admin** → `/login/` ✅ **Works with created admin user**
3. **View Dashboard** → `/dashboard/` ✅ **Shows organizer dashboard with next steps**
4. **Create Events** → `/events/` 🔄 **To be implemented**
5. **Manage Bookings** → `/bookings/` 🔄 **To be implemented**

### **For New Individual User:**
1. **Register User** → `/register/` ✅ **Creates user + personal tenant + schema automatically**
2. **Login** → `/login/` ✅ **Works with created user**
3. **View Dashboard** → `/dashboard/` ✅ **Shows attendee dashboard with next steps**
4. **Browse Events** → `/events/` 🔄 **To be implemented**
5. **Make Bookings** → `/bookings/` 🔄 **To be implemented**

---

## 🧪 **TESTING THE CURRENT SYSTEM:**

### **✅ Test User Registration:**
```
1. Go to: http://127.0.0.1:8000/register/
2. Fill form with any details (password validation disabled)
3. Result: User + Personal Tenant + Schema created automatically
4. Check: User becomes admin of their personal tenant
```

### **✅ Test Tenant Registration:**
```
1. Go to: http://127.0.0.1:8000/register-tenant/
2. Fill form with organization details
3. Result: Organization + Admin User + Schema created automatically
4. Check: All tables created in tenant schema
```

### **✅ Test Dashboard:**
```
1. Register a user or tenant
2. Login with credentials
3. Go to: http://127.0.0.1:8000/dashboard/
4. Result: Should show dashboard with tenant info and next steps
5. Check: No more AttributeError for tenant.events
```

### **✅ Test API Endpoints:**
```
List Tenants: GET http://127.0.0.1:8000/api/list-tenants/
Create Schema: POST http://127.0.0.1:8000/api/create-schema/
Body: tenant_slug=your-tenant-slug
```

### **✅ Test Schema Creation:**
```
1. Check PostgreSQL schemas in pgAdmin
2. Look for: tenant_techcorp-events, tenant_startup-hub, etc.
3. Verify: Each schema has events and bookings tables
4. Confirm: Proper tenant isolation
```

---

## 🛠️ **DEVELOPMENT NOTES:**

- **Password Validation**: Disabled for easy testing
- **Database**: PostgreSQL with schema-based multitenancy
- **Authentication**: Django's built-in auth system
- **Templates**: Basic HTML templates (Bootstrap styling)
- **API**: RESTful endpoints for schema management
- **Multitenancy**: Schema-based isolation (not row-level)
- **Auto Schema Creation**: Enabled for all registrations
- **Dashboard**: Fixed and working with proper context

---

## 📋 **QUICK REFERENCE:**

### **🔗 Most Used Endpoints:**
- **Home**: `GET /`
- **Register User**: `POST /register/`
- **Register Organization**: `POST /register-tenant/`
- **Login**: `POST /login/`
- **Dashboard**: `GET /dashboard/`
- **List Tenants API**: `GET /api/list-tenants/`
- **Create Schema API**: `POST /api/create-schema/`

### **🔑 Key Features:**
- ✅ **Automatic Schema Creation** for all registrations
- ✅ **Password Validation Disabled** for easy testing
- ✅ **Role-Based Dashboards** (organizer/attendee)
- ✅ **Multitenant Isolation** via PostgreSQL schemas
- ✅ **API Endpoints** for schema management

### **🚀 Ready for Next Phase:**
The system is now ready for implementing event management and booking functionality!
