#!/usr/bin/env python
# encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import logging
from celery import  task
from celery.utils.log import get_task_logger


from gevent import  monkey
monkey.patch_all()
import  gevent


from center.Amazon.Amazon_api  import Amazon_MWS

logger = get_task_logger(__name__)
log1 = logging.getLogger("test1")


@task
def get_amazon_report(store_obj,type, fileName):
    AMAZON_MWS = Amazon_MWS()
    gevent.joinall([gevent.spawn(AMAZON_MWS.get_product_report,store_obj,type,fileName)])
    # AMAZON_MWS.get_product_report(store_obj,type,fileName)