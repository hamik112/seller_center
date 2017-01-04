#!/usr/bin/env python
# encoding:utf-8

import os
import datetime
from gevent import  monkey
gevent.patch_all()
import  gevent


from center.Amazon.Amazon_api  import Amazon_MWS




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
        AMAZON_MWS  = Amazon_MWS()
        access_key  = 'AKIAI4QSPO5ISDC2GJYQ'
        secret_key  = '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'
        store_key   = 'A2TFDJE5MM2YVC'
        store_token = 'amzn.mws.2ea9e504-eb46-815c-bbe6-c19ea0ff9192'
        region = self.region
        store_obj = Stores(access_key=access_key, secret_key=secret_key, store_key=store_key, store_token=store_token,
                           region=region)
        type = '_GET_AFN_INVENTORY_DATA_'
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H')
        fileName = str(now) +  '_FBA.txt'
        if not os.path.exists(fileName):
            os.system("touch %s"%fileName)
        result = AMAZON_MWS.get_product_report(store_obj,type=type,fileName=fileName)
        print result, fileName


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

"""



