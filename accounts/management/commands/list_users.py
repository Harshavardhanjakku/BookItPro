from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'List all users and their current roles'

    def handle(self, *args, **options):
        users = User.objects.all().order_by('email')
        
        self.stdout.write(
            self.style.SUCCESS('\n📋 Current Users and Their Roles:\n')
        )
        
        for user in users:
            role_display = user.get_role_display()
            tenant_name = user.tenant.name if user.tenant else "No Organization"
            
            # Color coding for roles
            if user.role == 'admin':
                role_color = self.style.ERROR  # Red for admin
            elif user.role == 'manager':
                role_color = self.style.WARNING  # Yellow for manager
            else:
                role_color = self.style.SUCCESS  # Green for attendee
            
            self.stdout.write(
                f'👤 {user.email}'
            )
            self.stdout.write(
                f'   Name: {user.get_full_name() or "No Name"}'
            )
            self.stdout.write(
                f'   Role: {role_color(role_display)}'
            )
            self.stdout.write(
                f'   Organization: {tenant_name}'
            )
            self.stdout.write(
                f'   Joined: {user.date_joined.strftime("%Y-%m-%d %H:%M")}'
            )
            self.stdout.write('')
        
        self.stdout.write(
            self.style.SUCCESS(f'📊 Total Users: {users.count()}')
        )
