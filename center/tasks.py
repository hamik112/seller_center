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
from center.models import  InventoryReports




from center.Amazon.Amazon_api  import Amazon_MWS

logger = get_task_logger(__name__)
log = logging.getLogger("tasks")


utc = pytz.timezone("GMT")


@task
def get_amazon_report(store_obj,rep_type, fileName, line_id):
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






