#!/usr/bin/env python
# encoding:utf-8

import os
import pytz
import datetime
import random

from django.conf import settings


from center.dataService.create_xls import generate_path
from center.tasks import get_amazon_report, download_import_report_task
from center.models import InventoryReports
from manageApp.models import FilenameToStorename, StoreKeys
from center.dataService.center_share import dt_to_str


GENERATE_REPORT_PATH = settings.GENERATE_REPORT_PATH


utc = pytz.timezone("GMT")


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

    def get_inventory_report(self, report_type):
        try:
            user  = FilenameToStorename.objects.filter(email=self.username)[0]  #判断
            really_store = user.really_store
        except Exception, e:
            user = []
            really_store = "0"

        line_id = self.inventory_report_recorde(report_type)
        now = datetime.datetime.now().strftime("%m-%d-%Y")
        fileName = os.path.join(generate_path(GENERATE_REPORT_PATH),  "Inventory+Report+"+str(now) + '.txt')
        if not os.path.exists(fileName):
            os.system("touch %s"%fileName)

        if user and really_store != "0":
            try:
                store = StoreKeys.objects.filter(email=self.username)[0]
                access_key = store.access_key
                secret_key = store.secret_key
                store_key  = store.account_id
                store_token= store.mws_authtoken
            except Exception, e:
                store = ""
                access_key = ""
                secret_key = ""
                store_key = ""
                store_token = ""
            
            print "3" * 100
            print "user, really_store:", access_key, secret_key, store_key, store_token

            region = self.region
            store_obj = Stores(access_key=access_key, secret_key=secret_key,
                               store_key=store_key, store_token=store_token,
                               region=region)
            rep_type = '_GET_AFN_INVENTORY_DATA_'
            get_amazon_report.delay(store_obj,rep_type , fileName, line_id)
            print fileName
        #if really_store == "0":  #等于0，则是不是真实店铺
        else:
            print "1"*100
            print "不是真实店铺"
            username = self.username
            self.download_import_report(username,report_type, fileName,line_id)

    def download_import_report(self,username, report_type,  fileName, line_id):
        download_import_report_task.delay(username, report_type, fileName, line_id)
        pass


    def inventory_report_recorde(self, report_type):
        tmp_dict = {"username":self.username,
                    "report_type":report_type if report_type else "",
                    "date_time_request": dt_to_str(datetime.datetime.now(tz=utc)),
                    "date_time_completed": "Not Completed",   #== Not Completed if request submitted
                    "report_status": "1",   #Request Submitted
                    "batch_id": self.get_batch_id(),
                    }
        try:
            itr = InventoryReports(**tmp_dict)
            itr.save()
            id = itr.id
        except Exception, e:
            print str(e)
            id = ""
        print "="*100
        print "id: ", id
        return id

    def get_batch_id(self):
        return "500" + "".join([str(random.randrange(0,9)) for i in range(8)])


    def get_report_recorde(self, count=None, page=None):
        if not count and not page:
            count,page = 10, 1
        elif not count and page:
            count, page = 10, page
        elif count and not page:
            count, page = count, 1
        else:
            count, page = count, page 
        page, count = int(page) - 1, int(count)
        try:
            recored_list = InventoryReports.objects.filter(username=self.username).order_by("-id")[page * count:( page +1 ) * count]
        except Exception, e:
            print "get recorde error: "+str(e)
            recored_list = []
        return_recored_list = []
        for li in recored_list:
            tmp_dict = {}
            tmp_dict["report_type"] = ReportType().get_report_type(li.report_type)
            tmp_dict["date_time_request"] = li.date_time_request
            tmp_dict["date_time_completed"] = li.date_time_completed
            tmp_dict["batch_id"] = li.batch_id
            tmp_dict["report_status"] = li.report_status
            tmp_dict["fileName"] = str(li.fileName).strip()
            return_recored_list.append(tmp_dict)
        return list(return_recored_list)


class ReportType(object):
    def __init__(self):
        self.type_dict = {
            "107": "Inventory Report",
            "300": "Active Listings Report",
            "302": "Open Listings Report Lite",
            "303": "Open Listings Report Liter",
            "304": "Open Listings Report",
            "309": "Cancelled Listings Report",
            "312": "Sold Listings Report",
            "314": "Listing Quality and Suppressed Listing Report(NEW)",
            "315": "Referral Fee Preview Report (BETA)",
            "301": "Amazon-fulfilled Inventory Report",
            "321": "High Volume Listings Report"
        }

    def get_report_type(self, key):
        type_dict = self.type_dict
        return type_dict.get(key, "")

    def from_value_get_key(self, value):
        type_dict = self.type_dict
        for k in type_dict:
            if type_dict.get(k) == value:
                return k
        return ""








    



