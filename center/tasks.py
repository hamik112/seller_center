#!/usr/bin/env python
# encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import  datetime
import  pytz
import logging
from celery import  task
from celery.utils.log import get_task_logger

from center.dataService.center_share import dt_to_str
from center.dataService.statement_view_data import StatementViewData
from center.models import  InventoryReports, InventoryReportsData




from center.Amazon.Amazon_api  import Amazon_MWS

logger = get_task_logger(__name__)
log = logging.getLogger("tasks")


utc = pytz.timezone("GMT")


@task
def get_amazon_report(store_obj,rep_type, fileName, line_id):
    """task:真实店铺，去amazon获取信息, 请求有时候好慢"""
    AMAZON_MWS = Amazon_MWS()
    print "report tasks start ......"
    #gevent.joinall([gevent.spawn(AMAZON_MWS.get_product_report,store_obj,type,fileName)])
    try:
        result = AMAZON_MWS.get_product_report(store_obj,rep_type,fileName)
    except Exception, e:
        result = {"result": False, "error_message": str(e)}
        #print "AMAZON_MWS API Request Error: ",str(e)
        log.info("AMAZON_MWS API Request Error: ",str(e))
    if result.get("result", False) and line_id:
        try:
            fname = fileName.split("GENERATE_REPORT/")[1]
        except Exception, e:
            #print str(e)
            log.info(str(e))
            fname = ""
        try:
            InventoryReports.objects.filter(id=line_id).update(date_time_completed = dt_to_str(datetime.datetime.now(tz=utc)),
                                                               report_status = "Ready",
                                                               fileName = fname)
        except Exception, e:
            #print "rewrite InventoryReports Error: ", str(e)
            log.info("rewrite InventoryReports Error: ", str(e))
    else:
        #print result.get("result", True), result.get("error_message","")
        log.info(result.get("result", True), result.get("error_message",""))

@task
def download_import_report_task(username, report_type, fileName, line_id):
    """task:非真实店铺，从数据库获取, 数据量大的时候，好慢"""
    datas_list = InventoryReportsData.objects.filter(username=username).values("seller_sku","fulfillment_channel_sku","asin", "condition_type", "Warehouse_Condition_code", "Quantity_Available")
    with open(fileName, "w") as f:
        for line in datas_list:
            line_str = ""
            line_str += line.get("seller_sku","") + "\t"
            line_str += line.get("fulfillment_channel_sku", "") + "\t"
            line_str += line.get("asin", "") + "\t"
            line_str += line.get("condition_type", "") + " "
            line_str += line.get("Warehouse_Condition_code", "") + "\t"
            line_str += line.get("Quantity_Available", "") + "\n"
            f.write(line_str)

    #---
    try:
        InventoryReports.objects.filter(id=line_id).update(date_time_completed = dt_to_str(datetime.datetime.now(tz=utc)))
    except Exception, e:
        log.info("rewrite InventoryReports Error: ", str(e))
    




@task
def data_range_reports_tasks(username, post_dict, return_dict):
    """tasks: data_range_reports页面, 生成pdf部分,量大好慢,还卡死了整个server,所以用task"""
    print "+"*100
    print "task request:", username, post_dict
    result = StatementViewData(username, post_dict, return_dict).request_report()
    


