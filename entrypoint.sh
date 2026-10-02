#!/bin/sh
set -e

echo "==> Preparing Idesignweb Platform..."

# Run relational database migrations (SQLite side-store for auth and sessions)
echo "==> Running Django database migrations..."
python manage.py migrate --noinput

# Ensure production superuser credentials from environment
echo "==> Configuring superuser credentials from environment..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.contrib.auth.models import User
u = os.getenv('DJANGO_SUPERUSER_USERNAME') or os.getenv('ADMIN_USERNAME')
p = os.getenv('DJANGO_SUPERUSER_PASSWORD') or os.getenv('ADMIN_PASSWORD')
e = os.getenv('DJANGO_SUPERUSER_EMAIL') or os.getenv('ADMIN_EMAIL') or 'admin@idesignweb.co.ke'
if not e or '@' not in e or '.' not in e.split('@')[-1]:
    e = f\"{e.split('@')[0]}@idesignweb.co.ke\"
if u and p:
    user = User.objects.filter(username=u).first()
    if not user:
        user = User.objects.create_user(username=u, email=e, password=p)
    else:
        user.email = e
        user.set_password(p)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f'==> Verified superuser account: {u} ({e})')
else:
    print('==> DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD unset. Skipping superuser setup.')
"

# Ensure production public catalog and admin account from environment
echo "==> Initializing platform catalog and admin credentials..."
python manage.py seed_data || echo "==> Initialization step finished."


# Collect static assets for WhiteNoise
echo "==> Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn production server
echo "==> Starting Gunicorn WSGI server on 0.0.0.0:8000..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --access-logfile - \
    --error-logfile -
