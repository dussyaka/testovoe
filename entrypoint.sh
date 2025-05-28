#!/usr/bin/env bash

chown -R appuser:appuser /app/static/
python web/manage.py collectstatic --noinput
python web/manage.py migrate
python web/insertcitytodb.py
python -m gunicorn --chdir /app/web/ --bind 0.0.0.0:8000 --workers 1 web.wsgi:application
# for debug
#python manage.py runserver 0.0.0.0:8000