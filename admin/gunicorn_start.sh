#!/bin/bash
cd /var/www/backend/admin
source ../env/bin/activate
exec gunicorn djangoproject.wsgi:application \
  --bind 0.0.0.0:8050 \
  --workers 3 \
  --timeout 120
