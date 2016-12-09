#!/bin/bash

ps -ef | grep 'manage.py celery worker'  | awk -F  " " '{print $2}' | xargs kill -9
ps -ef | grep 'manage.py runserver'  | awk -F  " " '{print $2}' | xargs kill -9
echo "stop..."
