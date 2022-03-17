#!/usr/bin/env bash
sh -c "echo /opt/oracle/instantclient > /etc/ld.so.conf.d/oracle-instantclient.conf"

ldconfig

export LD_LIBRARY_PATH=/opt/oracle/instantclient:$LD_LIBRARY_PATH

python manage.py collectstatic --noinput

python manage.py migrate

gunicorn networkinfo.wsgi:application --bind 0.0.0.0:8000 --reload -w 4 --timeout 600