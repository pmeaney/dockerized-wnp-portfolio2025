#!/bin/bash

set -e

# Check if required variables are set
if [ -z "$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$DJANGO_SUPERUSER_EMAIL" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Error: Superuser environment variables not set"
    exit 1
fi

# Create superuser if not exists
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', 
                                '$DJANGO_SUPERUSER_EMAIL', 
                                '$DJANGO_SUPERUSER_PASSWORD')
"

python manage.py migrate

python manage.py runserver 0.0.0.0:8000