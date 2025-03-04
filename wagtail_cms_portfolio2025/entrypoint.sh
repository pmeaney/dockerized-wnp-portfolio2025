#!/bin/bash 
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput
else
    echo "Warning: Superuser environment variables not set"
    echo "Continuing without creating a superuser"
    echo "To create a superuser, set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD"
fi

# Collect static files if not already done
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run gunicorn for production
echo "Starting Gunicorn server..."
exec gunicorn wagtail_cms_portfolio2025.wsgi:application --bind 0.0.0.0:8000 --workers=4 --timeout=120