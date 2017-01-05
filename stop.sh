#!/bin/bash

ps -ef | grep 'manage.py celery worker'  | grep -v grep  | awk -F  " " '{print $2}' | xargs kill -9
#ps -ef | grep 'manage.py runserver'  | grep -v grep  | awk -F  " " '{print $2}' | xargs kill -9
ps -ef | grep 'gevent-monkey-patch --http :8009'  | grep -v grep  | awk -F  " " '{print $2}' | xargs kill -9



echo "stop..."
