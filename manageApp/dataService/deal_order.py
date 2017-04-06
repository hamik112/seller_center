#-*-coding:utf-8-*-
'''
Created on 2016年3月15日

@author: starmerx_008
'''
import datetime
import sys
import time

import os
from django.conf import  settings

from manageApp.models import FileUploadOther
from manageApp.tasks import deal_file
UPLOAD_PATH = settings.UPLOAD_PATH
reload(sys)
sys.setdefaultencoding('utf-8')

def write_file_other_handle(file_list):
    try:
        for fileobj in file_list:
            fname = fileobj.name
            filename = str(time.time()).replace(".", "") + "_" + fname
            file_path = os.path.join(get_path_other(UPLOAD_PATH), filename)
            with open(file_path, "wb+") as f:
                for chunk in fileobj.chunks():
                    f.write(chunk)
            result_filename = filename.split('.')[0] + '_handled.' + filename.split('.')[1]
            result_filepath = os.path.join(get_path_other(UPLOAD_PATH), result_filename)
            db_file_name = result_filename.split('_')[1]+'_'+result_filename.split('_')[2]
            obj = FileUploadOther.objects.create(file_name = db_file_name,file_path=result_filepath,status ='0')
            deal_file.delay(file_path,fname,result_filepath,obj)
    except Exception,e:
        raise e
def get_path_other(path):
    now_date = datetime.datetime.now()
    year = now_date.year
    month = now_date.month
    day = now_date.day
    one_path = os.path.join(path, str(year))
    second_path = os.path.join(one_path, str(month))
    third_path = os.path.join(second_path, str(day))
    if not os.path.exists(third_path):
        os.makedirs(third_path)
    return third_path