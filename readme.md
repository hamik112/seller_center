

1. pip install -r requirement.txt


2.   mysql> create database seller_center character set utf8;


3. 安装redis-server
  # yum install redis (#apt-get install redis-server)




启动:
1. #单独使用
    nohup python manage.py celery worker -q -c 4  --loglevel=info
    python manage.py runserver 0.0.0.0:8080


2. #配合nginx使用
    #./start







