#!/usr/bin/env python
# encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import  logging
from celery import  task
from celery.utils.log import get_task_logger

from manageApp.models import  StatementView, FilenameToStorename
from center.models import InventoryReportsData
from manageApp.dataService.tasks_util import update_file_statue, str_to_datetime
from manageApp.dataService.tasks_util import inventory_update_file_statue
from manageApp.dataService.deal_xls import read_xls
from manageApp.dataService.csv_to_excel import csv_to_xls

logger = get_task_logger(__name__)

log1 = logging.getLogger("tasks")


@task(max_retries=3,default_retry_delay=1 * 6)
def import_one_file_to_statement_view(file_path, filename):
    logger.info("running ...")
    print file_path, filename
    if filename.endswith(".csv"):
        file_path = csv_to_xls(file_path)
    try:
        datas = read_xls(file_path)
    except Exception, e:
        print str(e)
        datas = {"data": [],"statue": -1 ,"msg": "文件格式错误,请重新文件另外存为.xls文件再上传"}
    # filename = task_dict.get("filename", "")
    datas = datas.get("data", {})

    if isinstance(datas, dict) and  datas.get("statue", "") == -1 and datas.get("msg", ""):
        update_file_statue(filename, -1, error_msg=datas.get("msg", ""))
        return {"statue": -1, "msg": datas.get("msg", "")}

    value_list = []
    try:
        f_name = filename.split("__")[-1]
    except Exception, e:
        f_name = ""
        msg = "文件名错误!"
        update_file_statue(filename, -1, error_msg=msg)
        return {"statue": -1, "msg": msg}
    for dt in datas:
        if dt.get("name", "").lower() == "sheet1" or \
                        dt.get("name", "").lower() == "template" or \
                        dt.get("name","").replace(" ","") == f_name.split(".")[0].replace(" ", ""):
            value_list = dt.get("values", [])
            break
    if not value_list:
        try:
            value_list = datas[0].get("values", [])
        except Exception, e:
            msg = "没有找到文件!" + str(e)
            print msg
            log1.info(msg)
            update_file_statue(filename, -1, error_msg=msg)
    if not value_list:
        msg = "表格无数据或请查看是否在第一个sheet里面或查看sheet名称是sheet1"
        return {"statue": -1, "msg": msg}
        update_file_statue(filename, -1, error_msg=msg)
    if len(value_list[3]) > 20:
        header_list = value_list[0]
        datas_list = value_list[1:]
    else:
        header_list = value_list[7]
        datas_list = value_list[8:]
    need_header_list = ['date_time', 'settlement id', 'type', 'order id', 'sku', 'description', 'quantity',
                        'marketplace', 'fulfillment', 'order city', 'order state', 'order postal',
                        'product sales', "shipping credits", "gift wrap credits", "promotional rebates",
                        "sales tax collected", "selling fees", "fba fees", "other transaction fees",
                        "other", "total" ]
    header_dict = {}
    # print header_list, 
    header_num_list = [0, 1, 2,3,4,5,6,7,8,9,10, 11,12,13,14,15,16,17,18,19,20,21]
    header_dict = dict(zip(need_header_list,header_num_list))
    """
    #实在没办法，根据头部字段来判断位置，他们写的不统一，实在难搞，直接上数字
    for name in need_header_list:
        try:
            if name == "date_time":
                header_dict[name] = header_list.index("date/time")
            else:
                header_dict[name] = header_list.index(name)
        except :
            if name == "date_time":
                msg = "没有找到字段: date/time" 
            else:
                msg = "没有找到字段: " + str(name)
            update_file_statue(filename, -1, error_msg=msg)
            return {"statue": -1, "msg": msg}
    """
    # try:
    #     header_dict[u"店铺"] = header_list.index(u"店铺")
    # except Exception, e:
    #     msg = "没有找到字段: 店铺"
    #     update_file_statue(filename, -1, error_msg=msg)
    #     return {"statue": -1, "msg": msg}

    filename_split_list = filename.split("-")
    if len(filename_split_list) < 2:
        return {"statue": -1, "msg": "文件名错误:文件名格式不正确!"}
    serial_number = "-".join(filename.split("-")[:2])
    try:
        store_name = FilenameToStorename.objects.get(serial_number=serial_number).storename
    except Exception ,e:
        log1.info("filename: %s not found store_name"%str(filename))
        store_name = ""
    try:
        area  = filename.split(".")[0].split("-")[-1]
    except Exception, e:
        area = ""
    log1.info(len(value_list))
    n = 0
    for data_line in datas_list:
        log1.info("current: "+ str(n))
        n += 1
        tmp_dict = {"filename": filename}
        for name in need_header_list:
            # if name == u"店铺" or name == "店铺":
            #     tmp_dict["store_name"] = data_line[header_dict.get(name)]
            if name == "date_time":
                print data_line[header_dict.get("date_time")]
                tmp_dict["date_time"] = str_to_datetime(data_line[header_dict.get("date_time")])
            else:
                dict_name = name.replace(" ", "_")
                tmp_dict[dict_name] = data_line[header_dict.get(name)]
        tmp_dict["serial_number"] = serial_number
        tmp_dict["store_name"] = store_name
        tmp_dict["area"] = area
        try:
            stv = StatementView(**tmp_dict)
            stv.save()
        except Exception, e:
            print str(e)
            log1.info(str(e))
            try:
                StatementView.objects.filter(order_id=tmp_dict.get("order_id", "")).update(**tmp_dict)
            except Exception, e:
                msg = "存在重复记录, order_id是:"+str(tmp_dict.get("order_id", ""))
                log1.error(msg)
                update_file_statue(filename, -1, error_msg=msg)
                return {"statue": -1, "msg": str(e)}
    log1.info(str(n))
    update_file_statue(filename, 2)
    return {"statue": 0, "msg": ""}


@task(max_retries=3,default_retry_delay=1 * 6)
def inventory_import(datas, filename):
    datas = datas.get("data", [])
    username = filename.split("__")[0]    #所属用户，从文件名里面获取
    n = 0
    for line in datas:
        log1.info("current: "+ str(n))
        n += 1
        tmp_dict = {"sku":line[0], "asin":line[1],
                    "price":line[2], "quantity":line[3],
                    "filename":username}
        try:
            InventoryReportsData(**tmp_dict).save()
        except Exception, e:
            msg = "文件 %s 写入inveotry report错误: %s " % (filename,str(e))
            log1.error(msg)
            inventory_update_file_statue(filename,-1, error_msg=msg)
    log1.info(str(n))
    inventory_update_file_statue(filename, 2)
    return {"status": 0, "msg": ""}
