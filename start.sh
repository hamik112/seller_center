#!/bin/bash

python  change_auth_user_length.py &


#nohup python manage.py celery worker -q -c 2  --loglevel=info  >/dev/null 2>&1 &


#python manage.py celery worker -Q  download -l info    #这个是manageApp导入文件的worker 
#python manage.py celery worker -Q  celery  -l info     #这个是center下载文件的worker


#python manage.py runserver 0.0.0.0:8080 &

#nohup uwsgi  --http :8080 -M --process 4 --wsgi-file start_server.py &  #uwsgi 启动
#nohup uwsgi  --http :8009 -M --process 1 --wsgi-file start_server.py &  #uwsgi 启动

uwsgi -x seller_center_socket.xml &
