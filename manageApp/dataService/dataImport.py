#!/usr/bin/env python
# encoding:utf-8

import  datetime
import threading

from manageApp.dataService.deal_xls import read_xls
from manageApp.models import StatementView, UploadFileRecorde



class StatementViewImport(object):
    def __init__(self, files_list):
        self.files_list = files_list

    def import_files_to_statement_view(self):
        statue_list = []
        print self.files_list
        for filename in self.files_list:
            if filename.endswith(".xls") or filename.endswith(".xlsx"):
                try:
                    file_path = UploadFileRecorde.objects.filter(filename=filename)[0].file_path
                    print file_path
                    datas = read_xls(file_path)
                    print len(datas)
                    update_file_statue(filename,1)
                    # statue = self.import_one_file_to_statement_view(datas, filename)
                    t = threading.Thread(target=self.import_one_file_to_statement_view, args=(datas, filename))
                    t.start()
                    statue_dict = {"filename": filename, "statue": 0, "msg": ""}
                    # statue_dict = {"filename": filename, "statue": statue.get("statue"), "msg": statue.get("msg","")}
                except Exception, e:
                    statue_dict = {"filename": filename, "statue":-1, "msg": str(e)}
            else:
                print "not found .xls file"
                statue_dict = {"filename": filename, "statue": -1, "msg": u"文件不是.xls或.xlsx文件"}
            statue_list.append(statue_dict)
        return statue_list

    def import_one_file_to_statement_view(self, datas, filename):
        datas = datas.get("data",[])
        value_list = []
        try:
            f_name = filename.split("__")[-1]
        except Exception, e:
            f_name = ""
            msg = "文件名错误!"
            update_file_statue(filename, -1, error_msg=msg)
            return {"statue":-1, "msg": msg}
        for dt in datas:
            if dt.get("name", "").lower() == "sheet1" or dt.get("name", "").lower() == "template" or dt.get("name", "").replace(" ","") == f_name.split(".")[0].replace(" ",""):
                value_list = dt.get("values", [])
                break
        if not value_list:
            value_list = datas[0].get("values", [])
        if not value_list:
            msg = "表格无数据或请查看是否在第一个sheet里面或查看sheet名称是sheet1"
            return {"statue": -1, "msg": msg }
            update_file_statue(filename, -1, error_msg=msg)
        header_list = value_list[7]
        need_header_list = ['date_time', 'settlement id', 'type', 'order id','sku', 'description', 'quantity',
                            'marketplace','fulfillment', 'order city','order state','order postal',
                            'product sales', "shipping credits", "gift wrap credits", "promotional rebates",
                            "sales tax collected", "selling fees", "fba fees", "other transaction fees",
                            "other", "total", u"店铺"]
        header_dict = {}
        for name in need_header_list:
            try:
                if name == "date_time":
                    header_dict[name] = header_list.index("date/time")
                else:
                    header_dict[name] = header_list.index(name)
            except Exception,e :
                msg = u"没有找到字段:%s" % str(name)
                update_file_statue(filename, -1, error_msg=msg)
                return {"statue": -1, "msg": msg}
        serial_number = "-".join(filename.split("-")[:2])
        for data_line in value_list[8:]:
            tmp_dict = {"filename":filename}
            for name in need_header_list:
                if name == u"店铺" or name == "店铺":
                    tmp_dict["store_name"] = data_line[header_dict.get(name)]
                elif name == "date_time":
                    tmp_dict["date_time"] = self.str_to_datetime(data_line[header_dict.get("date_time")])
                else:
                    dict_name = name.replace(" ", "_")
                    tmp_dict[dict_name] = data_line[header_dict.get(name)]
            tmp_dict["serial_number"] = serial_number
            try:
                stv  = StatementView(**tmp_dict)
                stv.save()
            except Exception, e:
                try:
                    StatementView.objects.filter(order_id=tmp_dict.get("order_id","")).update(**tmp_dict)
                except Exception, e:
                    update_file_statue(filename, -1, error_msg=str(e))
                    return {"statue": -1, "msg": str(e)}
        update_file_statue(filename, 2)
        return {"statue":0, "msg":""}

    def str_to_datetime(self, date_str):
        time_zone = date_str.split(" ")[-1]
        try:
            dt =  datetime.datetime.strptime(date_str, "%b %d, %Y %I:%M:%S %p "+time_zone)
        except Exception, e:
            print e
            dt = datetime.datetime.now()
        return  dt





def update_file_statue(filename, statue, error_msg= ""):
    try:
        UploadFileRecorde.objects.filter(filename=filename).update(file_statue=str(statue), error_msg=error_msg)
    except Exception, e:
        print str(e)


def get_update_error_str(uid):
    try:
        error_msg = UploadFileRecorde.objects.filter(id=uid).values_list("error_msg", flat=True)[0]
    except Exception,e:
        print str(e)
        error_msg = u"没有找到这条记录!"
    return error_msg