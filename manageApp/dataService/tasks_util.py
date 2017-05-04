#!/usr/bin/env python
# encoding:utf-8

import  datetime
from manageApp.models import UploadFileRecorde, InventoryUploadRecorde
import re



def update_file_statue(filename, statue, error_msg= ""):
    try:
        UploadFileRecorde.objects.filter(filename=filename).update(file_statue=str(statue), error_msg=error_msg)
    except Exception, e:
        print str(e)





def get_update_file_statue(filename):
    try:
        file_statue = UploadFileRecorde.objects.filter(filename=filename).values_list("file_statue", flat=True)[0]
    except Exception,e :
        file_statue = ""
    return file_statue

#Mar 5, 2016 7:53:41 AM PST
def str_to_datetime( date_str):
    try:
        data_time_arr = re.split(r'\s+', date_str)
        time_zone = data_time_arr[-1]
        if data_time_arr[3].startswith('0'):
            arr_33 = data_time_arr[3].split(':')
            arr_33[0] = u'12'
            arr_33_str = ':'.join(arr_33)
            data_time_arr[3] = arr_33_str
        dt = datetime.datetime.strptime(' '.join(data_time_arr), "%b %d, %Y %I:%M:%S %p " + time_zone)
    except Exception, e:
        print e
        raise e
    return dt




def inventory_update_file_statue(filename, statue, error_msg= ""):
    try:
        InventoryUploadRecorde.objects.filter(filename=filename).update(file_statue=str(statue), error_msg=error_msg)
    except Exception, e:
        print str(e)


def inventory_get_update_file_statue(filename):
    try:
        file_statue = InventoryUploadRecorde.objects.filter(filename=filename).values_list("file_statue", flat=True)[0]
    except Exception,e :
        file_statue = ""
    return file_statue



