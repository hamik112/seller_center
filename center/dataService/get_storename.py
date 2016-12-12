#!/usr/bin/env python

from manageApp.models import FilenameToStorename


def get_storename(email):
    try:
        store_name = FilenameToStorename.objects.filter(email=email).values_list("storename", flat=True)[0]
    except Exception, e:
        store_name = ""
    print store_name
    return store_name


