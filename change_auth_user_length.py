#!/usr/bin/env python
# encoding:utf-8
import os
from django.db import connection, transaction


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SellerCenter.settings")




def my_custom_sql(sql_str):
    cursor = connection.cursor()
    # 数据修改操作——提交要求
    cursor.execute(sql_str)
    transaction.commit()


### 修改auth_user的字段长度，否则添加email作为username的时候会出现错误 ###

sql_str = "alter table auth_user modify column username varchar(50);"
my_custom_sql(sql_str)