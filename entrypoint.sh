#!/bin/sh
set -e

echo "==> Preparing Idesignweb Platform..."

# Run relational database migrations (SQLite side-store for auth and sessions)
echo "==> Running Django database migrations..."
python manage.py migrate --noinput

# Seed MongoDB collections & default accounts if not already present
echo "==> Checking seed data..."
python manage.py seed_data || echo "==> Seed data step finished."

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
