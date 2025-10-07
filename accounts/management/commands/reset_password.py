from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Reset password for a specific user'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of the user to reset password')
        parser.add_argument('--password', type=str, default='newpassword123', help='New password (default: newpassword123)')

    def handle(self, *args, **options):
        email = options['email']
        new_password = options['password']
        
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Password reset successfully for {user.email}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    f'🔑 New password: {new_password}'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'👤 User: {user.get_full_name() or "No Name"} ({user.get_role_display()})'
                )
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ User with email {email} not found'
                )
            )
