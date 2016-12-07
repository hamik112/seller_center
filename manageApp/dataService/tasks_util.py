#!/usr/bin/env python
# encoding:utf-8

import  datetime
from manageApp.models import UploadFileRecorde



def update_file_statue(filename, statue, error_msg= ""):
    try:
        UploadFileRecorde.objects.filter(filename=filename).update(file_statue=str(statue), error_msg=error_msg)
    except Exception, e:
        print str(e)


def str_to_datetime( date_str):
    time_zone = date_str.split(" ")[-1]
    try:
        dt = datetime.datetime.strptime(date_str, "%b %d, %Y %I:%M:%S %p " + time_zone)
    except Exception, e:
        print e
        dt = datetime.datetime.now()
    return dt
