from django.core.management.base import BaseCommand
from django.db import connection
from accounts.models import Tenant


class Command(BaseCommand):
    help = 'Create PostgreSQL schemas for all tenants'
    
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            tenants = Tenant.objects.all()
            
            for tenant in tenants:
                schema_name = f"tenant_{tenant.slug}"
                
                # Create schema if it doesn't exist
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
                
                # Create tables in the tenant schema
                self.create_tenant_tables(cursor, schema_name)
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created schema: {schema_name}')
                )
    
    def create_tenant_tables(self, cursor, schema_name):
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
                capacity INTEGER NOT NULL CHECK (capacity > 0),
                price DECIMAL(10,2) DEFAULT 0.00,
                status VARCHAR(20) DEFAULT 'draft',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                image VARCHAR(100),
                requirements TEXT,
                is_featured BOOLEAN DEFAULT FALSE,
                tenant_schema VARCHAR(100)
            )
        """)
        
        # Bookings table
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS "{schema_name}".bookings_booking (
                id SERIAL PRIMARY KEY,
                event_id INTEGER REFERENCES "{schema_name}".events_event(id),
                user_id INTEGER REFERENCES public.accounts_user(id),
                status VARCHAR(20) DEFAULT 'pending',
                booking_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                confirmation_code VARCHAR(20) UNIQUE,
                notes TEXT,
                special_requirements TEXT,
                amount_paid DECIMAL(10,2) DEFAULT 0.00,
                payment_status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                tenant_schema VARCHAR(100),
                CONSTRAINT unique_booking_per_user_event UNIQUE (event_id, user_id, tenant_schema)
            )
        """)
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS "{schema_name}".bookings_bookinghistory (
                id SERIAL PRIMARY KEY,
                booking_id INTEGER REFERENCES "{schema_name}".bookings_booking(id),
                old_status VARCHAR(20),
                new_status VARCHAR(20) NOT NULL,
                changed_by_id INTEGER REFERENCES public.accounts_user(id),
                reason TEXT,
                changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                tenant_schema VARCHAR(100)
            )
        """)
