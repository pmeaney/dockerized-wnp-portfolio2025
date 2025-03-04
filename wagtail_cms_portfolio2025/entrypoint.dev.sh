#!/bin/bash
set -e

# Print environment variables for debugging (redact sensitive info)
echo "==== DEBUGGING: Environment Variables ===="
echo "SQL_ENGINE: $SQL_ENGINE"
echo "SQL_DATABASE: $SQL_DATABASE"
echo "SQL_USER: $SQL_USER"
echo "SQL_HOST: $SQL_HOST"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "DJANGO_SUPERUSER_USERNAME: $DJANGO_SUPERUSER_USERNAME"
echo "DJANGO_SUPERUSER_EMAIL: $DJANGO_SUPERUSER_EMAIL"
echo "DJANGO_SUPERUSER_PASSWORD: [REDACTED]"
echo "========================================"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser only if it doesn't exist
echo "Checking superuser status..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    print('Creating superuser...');
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD');
    print('Superuser created successfully');
else:
    print('Superuser already exists, skipping creation');
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the development server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000