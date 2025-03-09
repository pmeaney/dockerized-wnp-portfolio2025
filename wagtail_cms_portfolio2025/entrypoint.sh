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


# Function to test if postgres is ready
postgres_ready() {
    python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(
        dbname="${SQL_DATABASE}",
        user="${SQL_USER}",
        password="${SQL_PASSWORD}",
        host="${SQL_HOST}",
        port="${SQL_PORT}"
    )
except psycopg2.OperationalError:
    sys.exit(1)
sys.exit(0)
END
}

# Wait for postgres to become available
echo "Waiting for PostgreSQL..."
RETRIES=10
until postgres_ready || [ $RETRIES -eq 0 ]; do
    echo "Waiting for PostgreSQL to become available... $((RETRIES)) remaining attempts..."
    RETRIES=$((RETRIES-1))
    sleep 3
done

if [ $RETRIES -eq 0 ]; then
    echo "Error: PostgreSQL not available after multiple attempts"
    exit 1
fi

echo "PostgreSQL is available!"


# Generate migrations
python manage.py makemigrations

# Apply migrations
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