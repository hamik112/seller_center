#!/usr/bin/env python
# encoding:utf-8

import os
import datetime


from django.conf import settings


from center.dataService.create_xls import generate_path
from center.tasks import get_amazon_report

GENERATE_REPORT_PATH = settings.GENERATE_REPORT_PATH



class Stores():
    def __init__(self,access_key,secret_key,store_key,store_token,region):
        self.access_key =access_key
        self.secret_key = secret_key
        self.store_key = store_key
        self.store_token = store_token
        self.region = region

class InventoryReport():
    def __init__(self, username, region = None):
        self.username = username
        self.region = region if region else "US"  #美国市场

    def get_inventory_report(self):

        access_key  = 'AKIAI4QSPO5ISDC2GJYQ'
        secret_key  = '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'
        store_key   = 'A2TFDJE5MM2YVC'
        store_token = 'amzn.mws.2ea9e504-eb46-815c-bbe6-c19ea0ff9192'
        region = self.region
        store_obj = Stores(access_key=access_key, secret_key=secret_key, store_key=store_key, store_token=store_token,
                           region=region)
        type = '_GET_AFN_INVENTORY_DATA_'
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H')
        fileName = os.path.join(generate_path(GENERATE_REPORT_PATH),  str(now) +  '_FBA.txt')
        if not os.path.exists(fileName):
            os.system("touch %s"%fileName)
        # gevent.joinall([gevent.spawn(AMAZON_MWS.get_product_report,store_obj,type,fileName)])
        # result = AMAZON_MWS.get_product_report(store_obj,type=type,fileName=fileName)
        get_amazon_report.delay(store_obj,type, fileName)
        print fileName


###
# gevent.spawn(f, *params)
###

"""
from gevent import monkey
monkey.patch_all()

import gevent
import requests


def f(url):
    print "GET: %s" % url
    try:
        req = requests.get(url, timeout=10)
        data = req.text
    except:
        data = ""
    print "%d bytes received from %s" %(len(data), url)


url_list =  ["https://www.python.org/", "https://www.yahoo.com","https://github.com", "https://www.baidu.com/", "https://www.google.com", "https://www.taobao.com"]

gevent.joinall([gevent.spawn(f, url) for url in url_list])



#!/usr/bin/env python
from gevent import monkey;
monkey.patch_all()
from gevent import wsgi
from mysite.wsgi import application
HOST = '127.0.0.1'
PORT = 8080# set spawn=None
for memcachewsgi.WSGIServer((HOST, PORT), application).serve_forever()
"""



