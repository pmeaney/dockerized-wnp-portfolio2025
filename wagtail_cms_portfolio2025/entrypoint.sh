#!/bin/bash 
set -e

# Debug: Show all environment variables
echo "==== DEBUGGING: Environment Variables ===="
echo "SQL_ENGINE: $SQL_ENGINE"
echo "SQL_DATABASE: $SQL_DATABASE"
echo "SQL_USER: $SQL_USER"
echo "SQL_HOST: $SQL_HOST"
echo "DJANGO_SUPERUSER_USERNAME: $DJANGO_SUPERUSER_USERNAME"
echo "DJANGO_SUPERUSER_EMAIL: $DJANGO_SUPERUSER_EMAIL"
echo "DJANGO_SUPERUSER_PASSWORD: [REDACTED]"
echo "========================================"

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
# echo "Starting Gunicorn server..."
# exec gunicorn wagtail_cms_portfolio2025.wsgi:application --bind 0.0.0.0:8000 --workers=4 --timeout=120

exec python manage.py runserver 0.0.0.0:8000