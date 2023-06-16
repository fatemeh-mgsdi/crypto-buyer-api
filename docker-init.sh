#!/bin/sh

python3 manage.py migrate
python3 manage.py create_superuser

gunicorn --bind :8000 crypto_buyer_api.wsgi:application

