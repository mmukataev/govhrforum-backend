#!/bin/bash
source /var/www/backend/env/bin/activate
exec gunicorn djangoproject.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120
