#!/bin/bash 

python  change_auth_user_length.py


python manage.py celery worker -q -c 4  --logievel=info  &


python manage.py runserver 0.0.0.0:8080 

