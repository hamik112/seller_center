#!/bin/bash

ps -ef | grep 'manage.py celery worker'  | grep -v grep  | awk -F  " " '{print $2}' | xargs kill -9
#ps -ef | grep 'manage.py runserver'  | grep -v grep  | awk -F  " " '{print $2}' | xargs kill -9
#ps -ef | grep 'http :8009'  | grep -v grep  | awk -F  " " '{print $2}' | xargs kill -9

ps -ef | grep 'uwsgi -x seller_center_socoket.xml'  | grep -v grep  | awk -F  " " '{print $2}' | xargs kill -9

echo "stop..."
