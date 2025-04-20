#!/usr/bin/env bash

# Exit on any error
set -e  

echo "Running Django migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
email = "admin@django.com"
password = "admin"
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
EOF

echo "Starting Gunicorn..."
exec gunicorn littlelemon.wsgi:application --bind 0.0.0.0:8000 --workers 2
