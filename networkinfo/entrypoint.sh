#!/usr/bin/env bash

python manage.py collectstatic --noinput

python manage.py migrate

gunicorn networkinfo.wsgi:application --bind 0.0.0.0:8000 --reload -w 4 --timeout 600