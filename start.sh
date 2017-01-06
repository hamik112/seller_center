#!/bin/bash

python  change_auth_user_length.py &


nohup python manage.py celery worker -q -c 4  --loglevel=info  &


#python manage.py runserver 0.0.0.0:8080 &

#uwsgi  --http :8080 -M --process 4 --wsgi-file start_server.py &  #uwsgi 启动
nohup uwsgi  --http :8009 -M --process 1 --wsgi-file start_server.py &  #uwsgi 启动

#uwsgi -x seller_center_socoket.xml &
