#! /bin/sh

python3 /usr/src/adminsite/networkinfo/manage.py makemigrations --no-input

python3 /usr/src/adminsite/networkinfo/manage.py migrate --no-input

python3 /usr/src/adminsite/networkinfo/manage.py runserver 0.0.0.0:8000

