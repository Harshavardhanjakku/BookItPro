from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Fix existing users roles based on email patterns'

    def handle(self, *args, **options):
        # Fix specific users based on your requirements
        users_to_fix = [
            {
                'email': 'himanshu@gmail.com',
                'role': 'manager',
                'description': 'Event Manager'
            },
            {
                'email': 'user1@gmail.com', 
                'role': 'attendee',
                'description': 'Attendee'
            }
        ]
        
        for user_data in users_to_fix:
            try:
                user = User.objects.get(email=user_data['email'])
                old_role = user.role
                user.role = user_data['role']
                user.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Updated {user.email}: {old_role} → {user_data["role"]} ({user_data["description"]})'
                    )
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ User with email {user_data["email"]} not found'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 User role updates completed!')
        )
