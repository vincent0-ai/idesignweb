"""
Management command to guarantee administrator account initialization from environment variables.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dotenv import load_dotenv
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Initializes or updates the Django superuser account from environment variables'

    def handle(self, *args, **options):
        # Load environment files if present
        for env_path in [Path('/app/.env'), Path('.env'), Path(__file__).resolve().parents[4] / '.env']:
            if env_path.exists():
                load_dotenv(env_path)

        username = os.getenv('DJANGO_SUPERUSER_USERNAME') or os.getenv('ADMIN_USERNAME')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD') or os.getenv('ADMIN_PASSWORD')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL') or os.getenv('ADMIN_EMAIL') or 'admin@idesignweb.co.ke'

        # Sanitize email (e.g. admin@idesignweb -> admin@idesignweb.co.ke)
        if not email or '@' not in email or '.' not in email.split('@')[-1]:
            prefix = email.split('@')[0] if '@' in email else email
            email = f"{prefix}@idesignweb.co.ke"

        if username and password:
            self.stdout.write(f"Configuring superuser '{username}' ({email})...")
            user = User.objects.filter(username=username).first()
            if not user:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f"Created new superuser: {username}"))
            else:
                user.email = email
                user.set_password(password)
                self.stdout.write(self.style.SUCCESS(f"Updated password for existing user: {username}"))

            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()

            total_users = User.objects.count()
            user_list = list(User.objects.values_list('username', flat=True))
            self.stdout.write(self.style.SUCCESS(f"Superuser active. Database users ({total_users}): {user_list}"))
        else:
            self.stdout.write("DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set in environment. Skipping.")
