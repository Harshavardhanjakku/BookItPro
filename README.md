# 🎉 BookItPro - Enterprise Event Booking Platform

<div align="center">

![BookItPro Logo](https://img.shields.io/badge/BookItPro-Event%20Booking%20Platform-blue?style=for-the-badge&logo=calendar)

**A powerful, multitenant event booking and management system built with Django**

[![Python](https://img.shields.io/badge/Python-3.11+-green?style=flat&logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2+-green?style=flat&logo=django)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=flat&logo=postgresql)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)

[🚀 Quick Start](#-quick-start) • [📚 Documentation](#-documentation) • [🔗 API Reference](#-api-reference) • [🤝 Contributing](#-contributing)

</div>

---

## 📖 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick Start](#-quick-start)
- [📚 Documentation](#-documentation)
- [🔗 API Reference](#-api-reference)
- [👥 User Roles](#-user-roles)
- [🛠️ Development](#️-development)
- [🧪 Testing](#-testing)
- [📊 Database Schema](#-database-schema)
- [🔒 Security](#-security)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 Overview

**BookItPro** is a comprehensive, enterprise-grade event booking and management platform designed for organizations of all sizes. Built with Django and PostgreSQL by **Jakku Harshavardhan**, it provides a robust multitenant architecture that allows multiple organizations to manage their events independently while sharing the same infrastructure.

### 🎯 Key Benefits

- **🏢 Multitenant Architecture**: Complete data isolation between organizations
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **🔐 Role-Based Access Control**: Granular permissions for different user types
- **📊 Real-time Analytics**: Comprehensive reporting and statistics
- **🔄 Auto Schema Management**: Automatic database schema creation for new tenants
- **💳 Payment Ready**: Built-in payment tracking and management
- **📧 Email Integration**: Automated notifications and confirmations

---

## ✨ Features

### 🎪 Event Management
- **Create & Manage Events**: Full CRUD operations for events
- **Event Types**: Categorize events (conferences, workshops, webinars, etc.)
- **Rich Event Details**: Images, descriptions, requirements, and special instructions
- **Capacity Management**: Set and track event capacity limits
- **Pricing**: Support for free and paid events
- **Event Status**: Draft, published, cancelled, and completed states

### 📅 Booking System
- **Easy Booking**: One-click event booking for attendees
- **Booking Management**: View, update, and cancel bookings
- **Confirmation Codes**: Unique codes for each booking
- **Booking History**: Complete audit trail of booking changes
- **Capacity Tracking**: Real-time availability updates
- **Special Requirements**: Handle attendee special needs

### 👥 User Management
- **Multiple User Types**: Organizers, Event Managers, and Attendees
- **Personal Tenants**: Individual users get their own event space
- **Organization Tenants**: Companies can manage multiple events
- **Profile Management**: Complete user profile system
- **Password Reset**: Secure password recovery system

### 🏢 Multitenant Features
- **Schema Isolation**: Each tenant has its own database schema
- **Automatic Provisioning**: New tenants get schemas created automatically
- **Tenant Management**: API endpoints for tenant operations
- **Data Security**: Complete separation between tenant data

### 📊 Analytics & Reporting
- **Event Statistics**: Track event performance and attendance
- **Booking Analytics**: Monitor booking trends and patterns
- **User Insights**: Understand user behavior and preferences
- **Real-time Dashboards**: Live updates on key metrics

---

## 🏗️ Architecture

### 🎨 Technology Stack

```
Frontend:     HTML5, CSS3, JavaScript, Bootstrap 5
Backend:      Django 5.2+, Python 3.11+
Database:     PostgreSQL with Schema-based Multitenancy
Authentication: Django's built-in auth system
File Storage: Local/Cloud storage for event images
API:          RESTful API endpoints
```

### 🏛️ System Architecture

```mermaid
graph TB
    A[User Interface] --> B[Django Views]
    B --> C[Business Logic]
    C --> D[Models Layer]
    D --> E[PostgreSQL Database]
    
    F[Tenant A Schema] --> E
    G[Tenant B Schema] --> E
    H[Tenant C Schema] --> E
    
    I[API Endpoints] --> C
    J[Admin Interface] --> C
    
    K[Authentication] --> B
    L[Middleware] --> B
```

### 🔄 Multitenant Architecture

BookItPro uses **schema-based multitenancy** where each organization gets its own PostgreSQL schema:

- **Public Schema**: Shared data (users, tenants, authentication)
- **Tenant Schemas**: Isolated data (events, bookings, event types)
- **Automatic Routing**: Middleware automatically routes to correct schema
- **Data Isolation**: Complete separation between tenant data

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.11+**
- **PostgreSQL 12+**
- **Git**
- **Virtual Environment** (recommended)

### ⚡ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Harshavardhanjakku/BookItPro.git
   cd BookItPro
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv bookitpro_env
   
   # Windows
   bookitpro_env\Scripts\activate
   
   # macOS/Linux
   source bookitpro_env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb bookitpro_db
   
   # Run migrations
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - **Main App**: http://127.0.0.1:8000
   - **Admin Panel**: http://127.0.0.1:8000/admin

### 🎯 First Steps

1. **Register an Organization**
   - Go to `/register-tenant/`
   - Fill in organization details
   - System automatically creates admin user and schema

2. **Login as Admin**
   - Use the created admin credentials
   - Access the organizer dashboard

3. **Create Event Types**
   - Navigate to `/events/types/`
   - Add categories (Conference, Workshop, Webinar, etc.)

4. **Create Your First Event**
   - Go to `/events/create/`
   - Fill in event details
   - Publish the event

5. **Test Booking**
   - Register as an attendee
   - Browse events and make a booking

---

## 📚 Documentation

### 🏠 Core Pages

| Page | URL | Description | Access Level |
|------|-----|-------------|--------------|
| **Home** | `/` | List of available organizations | Public |
| **Login** | `/login/` | User authentication | Public |
| **Register User** | `/register/` | Individual user registration | Public |
| **Register Organization** | `/register-tenant/` | Organization registration | Public |
| **Dashboard** | `/dashboard/` | User dashboard | Authenticated |
| **Profile** | `/profile/` | User profile management | Authenticated |

### 🎪 Event Management

| Page | URL | Description | Access Level |
|------|-----|-------------|--------------|
| **Event List** | `/events/` | Browse all events | Authenticated |
| **Event Detail** | `/events/{id}/` | View event details | Authenticated |
| **Create Event** | `/events/create/` | Create new event | Organizer |
| **Edit Event** | `/events/{id}/edit/` | Edit existing event | Organizer |
| **Delete Event** | `/events/{id}/delete/` | Delete event | Organizer |
| **Event Types** | `/events/types/` | Manage event categories | Organizer |

### 📅 Booking Management

| Page | URL | Description | Access Level |
|------|-----|-------------|--------------|
| **My Bookings** | `/bookings/` | User's bookings | Authenticated |
| **Booking Detail** | `/bookings/{id}/` | View booking details | Owner/Organizer |
| **Create Booking** | `/bookings/create/{event_id}/` | Book an event | Authenticated |
| **Cancel Booking** | `/bookings/{id}/cancel/` | Cancel booking | Owner |
| **Admin Bookings** | `/bookings/admin/` | Manage all bookings | Organizer |

### 🔧 Management Commands

```bash
# Create schemas for all existing tenants
python manage.py create_tenant_schemas

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser
```

---

## 🔗 API Reference

### 🔐 Authentication Endpoints

#### **POST** `/login/`
Authenticate user and create session.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** Redirects to dashboard on success

---

#### **POST** `/register/`
Register new individual user with personal tenant.

**Request Body:**
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

**Response:** Redirects to login page with success message

**Features:**
- ✅ Creates user account
- ✅ Creates personal tenant: "John Doe's Events"
- ✅ Creates schema: `tenant_john-doe-events`
- ✅ Makes user admin of their personal tenant
- ✅ Creates all necessary tables in schema

---

#### **POST** `/register-tenant/`
Register new organization with admin user.

**Request Body:**
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

**Response:** Redirects to login page with success message

**Features:**
- ✅ Creates organization/tenant
- ✅ Creates admin user for organization
- ✅ Creates schema: `tenant_my-company`
- ✅ Creates all necessary tables in schema

---

### 🏢 Tenant Management API

#### **GET** `/api/list-tenants/`
Get all active tenants and their information.

**Response:**
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

---

#### **POST** `/api/create-schema/`
Create database schema for specific tenant.

**Request Body:**
```json
{
  "tenant_slug": "techcorp-events"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully created schema: tenant_techcorp-events",
  "schema_name": "tenant_techcorp-events",
  "tenant_name": "TechCorp Events"
}
```

---

### 🎪 Event Management API

#### **GET** `/events/api/stats/`
Get event statistics for current tenant.

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_events": 25,
    "active_events": 20,
    "upcoming_events": 15,
    "event_types": [
      {
        "name": "Conference",
        "count": 10,
        "icon": "fas fa-users"
      },
      {
        "name": "Workshop",
        "count": 8,
        "icon": "fas fa-tools"
      }
    ]
  }
}
```

---

### 📅 Booking Management API

#### **GET** `/bookings/api/stats/`
Get booking statistics for current tenant.

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_bookings": 150,
    "confirmed_bookings": 120,
    "pending_bookings": 20,
    "cancelled_bookings": 10,
    "event_bookings": [
      {
        "event__title": "Python Conference 2024",
        "booking_count": 45
      },
      {
        "event__title": "Django Workshop",
        "booking_count": 30
      }
    ]
  }
}
```

---

## 👥 User Roles

### 👑 **Organizer Admin**
- **Permissions**: Full access to all features
- **Capabilities**:
  - Create, edit, and delete events
  - Manage all bookings
  - Access to all tenant data
  - Create and manage event types
  - View comprehensive analytics
  - Manage user permissions

### 👨‍💼 **Event Manager**
- **Permissions**: Event management focused
- **Capabilities**:
  - Create and edit events
  - View booking statistics
  - Manage event types
  - Cannot access user management
  - Limited analytics access

### 👤 **Attendee/User**
- **Permissions**: Booking and viewing only
- **Capabilities**:
  - Browse and search events
  - Book and cancel bookings
  - View own booking history
  - Update personal profile
  - Cannot create or manage events

---

## 🛠️ Development

### 📁 Project Structure

```
BookItPro/
├── accounts/                 # User management and authentication
│   ├── models.py            # User and Tenant models
│   ├── views.py             # Authentication views
│   ├── forms.py             # User forms
│   └── urls.py              # Account URLs
├── events/                   # Event management
│   ├── models.py            # Event and EventType models
│   ├── views.py             # Event views
│   ├── forms.py             # Event forms
│   └── urls.py              # Event URLs
├── bookings/                 # Booking management
│   ├── models.py            # Booking models
│   ├── views.py             # Booking views
│   ├── forms.py             # Booking forms
│   └── urls.py              # Booking URLs
├── bookitpro_project/        # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── multitenant.py       # Multitenant utilities
│   └── tenant_middleware.py # Tenant routing middleware
├── templates/                # HTML templates
├── static/                   # Static files (CSS, JS, images)
├── media/                    # User uploaded files
└── manage.py                 # Django management script
```

### 🔧 Development Setup

1. **Environment Variables**
   ```bash
   # Create .env file
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://user:password@localhost/bookitpro_db
   ```

2. **Database Configuration**
   ```python
   # settings.py
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'bookitpro_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

### 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test events
python manage.py test bookings

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### 🔍 Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

---

## 📊 Database Schema

### 🏗️ Core Models

#### **Tenant Model**
```python
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
```

#### **User Model**
```python
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Organizer Admin'),
        ('manager', 'Event Manager'),
        ('attendee', 'Attendee'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
```

#### **Event Model**
```python
class Event(TenantAwareModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='events/', blank=True)
```

#### **Booking Model**
```python
class Booking(TenantAwareModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    booking_date = models.DateTimeField(default=timezone.now)
    confirmation_code = models.CharField(max_length=20, unique=True)
    notes = models.TextField(blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)
```

### 🔄 Multitenant Schema Structure

```
PostgreSQL Database:
├── public (shared schema)
│   ├── accounts_tenant
│   ├── accounts_user
│   └── django_migrations
├── tenant_org1 (isolated schema)
│   ├── events_eventtype
│   ├── events_event
│   ├── bookings_booking
│   └── bookings_bookinghistory
└── tenant_org2 (isolated schema)
    ├── events_eventtype
    ├── events_event
    ├── bookings_booking
    └── bookings_bookinghistory
```

---

## 🔒 Security

### 🛡️ Security Features

- **🔐 Authentication**: Django's built-in authentication system
- **🔑 Authorization**: Role-based access control (RBAC)
- **🏢 Tenant Isolation**: Complete data separation between organizations
- **🛡️ CSRF Protection**: Cross-site request forgery protection
- **🔒 SQL Injection Prevention**: Django ORM protection
- **📝 Input Validation**: Comprehensive form validation
- **🔐 Password Security**: Secure password hashing
- **📧 Email Verification**: Optional email verification system

### 🔐 Security Best Practices

1. **Environment Variables**: Store sensitive data in environment variables
2. **HTTPS**: Use HTTPS in production
3. **Database Security**: Use strong database credentials
4. **Regular Updates**: Keep dependencies updated
5. **Access Logging**: Monitor access patterns
6. **Backup Strategy**: Regular database backups

---

## 🚀 Deployment

### 🐳 Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "bookitpro_project.wsgi:application"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:pass@db:5432/bookitpro
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=bookitpro
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### ☁️ Production Deployment

1. **Environment Setup**
   ```bash
   # Install production dependencies
   pip install gunicorn psycopg2-binary
   
   # Set environment variables
   export DEBUG=False
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URL=postgresql://user:pass@host:5432/db
   ```

2. **Database Migration**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn bookitpro_project.wsgi:application --bind 0.0.0.0:8000
   ```

### 🌐 Web Server Configuration

#### **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /static/ {
        alias /path/to/static/files/;
    }
    
    location /media/ {
        alias /path/to/media/files/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🤝 Contributing

We welcome contributions to BookItPro! Here's how you can help:

### 🚀 Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/Harshavardhanjakku/BookItPro.git
   cd BookItPro
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes**
   - Write clean, documented code
   - Add tests for new features
   - Update documentation

4. **Commit Changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open Pull Request**

### 📝 Contribution Guidelines

- **Code Style**: Follow PEP 8 and Django conventions
- **Testing**: Add tests for new features
- **Documentation**: Update README and docstrings
- **Issues**: Use GitHub issues for bug reports
- **Discussions**: Use GitHub discussions for questions

### 🐛 Bug Reports

When reporting bugs, please include:

- **Environment**: Python version, Django version, OS
- **Steps to Reproduce**: Clear, numbered steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Screenshots**: If applicable
- **Error Messages**: Full error traceback

### 💡 Feature Requests

For feature requests, please include:

- **Use Case**: Why is this feature needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other solutions considered
- **Additional Context**: Any other relevant information

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 📋 License Summary

- ✅ **Commercial Use**: Use in commercial projects
- ✅ **Modification**: Modify and adapt the code
- ✅ **Distribution**: Distribute the software
- ✅ **Private Use**: Use in private projects
- ❌ **Liability**: No warranty or liability
- ❌ **Warranty**: No warranty provided

---

## 📞 Support & Contact

### 🆘 Getting Help

- **📚 Documentation**: Check this README and inline documentation
- **🐛 Issues**: Report bugs on [GitHub Issues](https://github.com/Harshavardhanjakku/BookItPro/issues)
- **💬 Discussions**: Ask questions on [GitHub Discussions](https://github.com/Harshavardhanjakku/BookItPro/discussions)
- **📧 Email**: Contact at jakkuharshavardhan2004@gmail.com

### 🌟 Show Your Support

If you find BookItPro helpful, please:

- ⭐ **Star the Repository**
- 🍴 **Fork the Project**
- 🐛 **Report Issues**
- 💡 **Suggest Features**
- 📢 **Share with Others**

---

<div align="center">

**Made with ❤️ by Jakku Harshavardhan**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=flat&logo=github)](https://github.com/Harshavardhanjakku/BookItPro)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://linkedin.com/in/harshavardhanjakku)

</div>

---

*Last updated: January 2024*