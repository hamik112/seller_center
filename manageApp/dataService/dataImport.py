#!/usr/bin/env python
# encoding:utf-8

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
                    statue = self.import_one_file_to_statement_view(datas)
                    statue_dict = {"filename": filename, "statue": statue.get("statue"), "msg": statue.get("msg","")}
                except Exception, e:
                    statue_dict = {"filename": filename, "statue":-1, "msg": str(e)}
            else:
                print "not found .xls file"
                statue_dict = {"filename": filename, "statue": -1, "msg": u"文件不是.xls或.xlsx文件"}
            statue_list.append(statue_dict)
        return statue_list

    def import_one_file_to_statement_view(self, datas):
        datas = datas.get("data",[])
        value_list = []
        for dt in datas:
            if dt.get("name", "").lower() == "sheet1" or dt.get("name", "").lower() == "template":
                value_list = dt.get("values", [])
                break
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
                return {"statue": -1, "msg": u"没有找到字段:%s" % str(name)}
        print header_dict
        for data_line in value_list[8:]:
            tmp_dict = {}
            for name in need_header_list:
                if name == u"店铺" or name == "店铺":
                    tmp_dict["store_name"] = data_line[header_dict.get(name)]
                elif name == "date_time":
                    print name , header_dict.get("date_time")
                    tmp_dict["date_time"] = data_line[header_dict.get("date_time")]
                else:
                    dict_name = name.replace(" ", "_")
                    tmp_dict[dict_name] = data_line[header_dict.get(name)]
            try:
                stv  = StatementView(**tmp_dict)
                stv.save()
            except Exception, e:
                return {"statue": -1, "msg": str(e)}
        return {"statue":0, "msg":""}

