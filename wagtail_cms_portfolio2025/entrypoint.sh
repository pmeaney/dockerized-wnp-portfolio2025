#!/bin/bash
set -e

# Print environment variables for debugging (redact sensitive info)
echo "==== DEBUGGING: Environment Variables ===="
echo "SQL_ENGINE: $SQL_ENGINE"
echo "SQL_DATABASE: $SQL_DATABASE"
echo "SQL_USER: $SQL_USER"
echo "SQL_HOST: $SQL_HOST"
echo "DJANGO_SUPERUSER_USERNAME: $DJANGO_SUPERUSER_USERNAME"
echo "DJANGO_SUPERUSER_EMAIL: $DJANGO_SUPERUSER_EMAIL"
echo "DJANGO_SUPERUSER_PASSWORD: [REDACTED]"
echo "========================================"

# Check if PostgreSQL is ready
echo "Checking if PostgreSQL is ready..."
max_attempts=10
attempt=1

while [ $attempt -le $max_attempts ]; do
    echo "Connection attempt $attempt/$max_attempts"
    
    # Use PGPASSWORD environment variable to avoid password prompt
    export PGPASSWORD=$SQL_PASSWORD
    
    # Try to connect to PostgreSQL
    if pg_isready -h $SQL_HOST -p ${SQL_PORT:-5432} -U $SQL_USER -d $SQL_DATABASE -t 1; then
        echo "PostgreSQL is ready!"
        break
    else
        echo "PostgreSQL is not ready yet..."
    fi
    
    # Exit if we've reached the maximum attempts
    if [ $attempt -eq $max_attempts ]; then
        echo "Failed to connect to PostgreSQL after $max_attempts attempts"
        exit 1
    fi
    
    # Wait before the next attempt
    echo "Waiting 3 seconds before next attempt..."
    sleep 3
    attempt=$((attempt+1))
done


echo "Creating & Applying database migrations..."
python manage.py makemigrations portfolio
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

# Start the Wagtail server
echo "Starting Wagtail server..."
exec gunicorn wagtail_cms_portfolio2025.wsgi:application --bind 0.0.0.0:8000 --workers=4 --timeout=120
# OR if using runserver instead:
# exec python manage.py runserver 0.0.0.0:8000