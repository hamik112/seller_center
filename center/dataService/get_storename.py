#!/usr/bin/env python

from manageApp.models import FilenameToStorename


def get_storename(email):
    try:
        store_name = FilenameToStorename.objects.filter(email=email).values_list("storename", flat=True)[0]
    except Exception, e:
        store_name = ""
    print store_name
    return store_name


def get_serial_number(email):
    try:
        serial_number = FilenameToStorename.objects.filter(email=email).values_list("serial_number", flat=True)[0]
    except Exception, e:
        serial_number = ""
    print serial_number
    return serial_number