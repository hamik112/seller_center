

1. pip install -r requirement.txt


2.   mysql> create database seller_center character set utf8;


3. 安装redis-server
  # yum install redis (#apt-get install redis-server)
   # nohup redis-server /etc/redis.conf   >/dev/null 2>&1 &


启动:
1. #单独使用
    nohup python manage.py celery worker -q -c 4  --loglevel=info
    python manage.py runserver 0.0.0.0:8080


2. #配合nginx使用
    #./start



使用supervisord 部署监控,挂掉后自动重启

  #pip install supervisor
  #echo_supervisord_conf > supervisord.conf
  修改supervisord.conf
  在文件最后面添加

        [program:celery]
        command=python manage.py celery worker -q -c 2
        directory=.
        stdout_logfile=center/log/celery.log
        autostart=true
        autorestart=true
        redirect_stderr=true
        stopsignal=QUIT

        [program:mredis]
        command=redis-server  /etc/redis.conf   ; //需要执行的命令
        autostart=true                          ;//supervisor启动的时候是否随着同时启动
        autorestart=true                        ; //当程序跑出exit的时候，这个program会自动重启
        startsecs=3                             ;//程序重启时候停留在runing状态的秒数
        stdout_logfile=center/log/redis.log     ;; 使用这个log，可以查看redis-server 启动失败的原因
        redirect_stderr=true
        exitcodes=1

  (3)启动
   #supervisorctl start mredis
   #supervisorctl start celery






