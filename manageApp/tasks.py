#!/usr/bin/env python
# encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from celery import  task
from celery.utils.log import get_task_logger

from manageApp.models import  StatementView
from manageApp.dataService.tasks_util import update_file_statue, str_to_datetime

logger = get_task_logger(__name__)



@task
def import_one_file_to_statement_view(task_dict):
    logger.info("running ...")
    datas = task_dict.get("datas",{})
    filename = task_dict.get("filename", "")
    datas = datas.get("data", {})

    print datas
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
            update_file_statue(filename, -1, error_msg=msg)
    if not value_list:
        msg = "表格无数据或请查看是否在第一个sheet里面或查看sheet名称是sheet1"
        return {"statue": -1, "msg": msg}
        update_file_statue(filename, -1, error_msg=msg)
    header_list = value_list[7]
    need_header_list = ['date_time', 'settlement id', 'type', 'order id', 'sku', 'description', 'quantity',
                        'marketplace', 'fulfillment', 'order city', 'order state', 'order postal',
                        'product sales', "shipping credits", "gift wrap credits", "promotional rebates",
                        "sales tax collected", "selling fees", "fba fees", "other transaction fees",
                        "other", "total" ]
    header_dict = {}
    for name in need_header_list:
        try:
            if name == "date_time":
                header_dict[name] = header_list.index("date/time")
            else:
                header_dict[name] = header_list.index(name)
        except :
            msg = "没有找到字段: " + str(name)
            update_file_statue(filename, -1, error_msg=msg)
            return {"statue": -1, "msg": msg}
    try:
        header_dict[u"店铺"] = header_list.index(u"店铺")
    except Exception, e:
        msg = "没有找到字段: 店铺"
        update_file_statue(filename, -1, error_msg=msg)
        return {"statue": -1, "msg": msg}


    filename_split_list = filename.split("-")
    if len(filename_split_list) < 2:
        return {"statue": -1, "msg": "文件名错误:文件名格式不正确!"}
    serial_number = "-".join(filename.split("-")[:2])
    for data_line in value_list[8:]:
        tmp_dict = {"filename": filename}
        for name in need_header_list:
            if name == u"店铺" or name == "店铺":
                tmp_dict["store_name"] = data_line[header_dict.get(name)]
            elif name == "date_time":
                tmp_dict["date_time"] = str_to_datetime(data_line[header_dict.get("date_time")])
            else:
                dict_name = name.replace(" ", "_")
                tmp_dict[dict_name] = data_line[header_dict.get(name)]
        tmp_dict["serial_number"] = serial_number
        try:
            stv = StatementView(**tmp_dict)
            stv.save()
        except Exception, e:
            try:
                StatementView.objects.filter(order_id=tmp_dict.get("order_id", "")).update(**tmp_dict)
            except Exception, e:
                update_file_statue(filename, -1, error_msg=str(e))
                return {"statue": -1, "msg": str(e)}
    update_file_statue(filename, 2)
    return {"statue": 0, "msg": ""}


