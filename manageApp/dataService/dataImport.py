#!/usr/bin/env python
# encoding:utf-8

import  datetime
import threading



from manageApp.dataService.deal_xls import read_xls
from manageApp.models import StatementView, UploadFileRecorde

from manageApp.tasks import import_one_file_to_statement_view
from manageApp.dataService.tasks_util import update_file_statue, get_update_file_statue


class StatementViewImport(object):
    def __init__(self, files_list):
        self.files_list = files_list

    def import_files_to_statement_view(self):
        statue_list = []
        print self.files_list
        for filename in self.files_list:
            if get_update_file_statue(filename) == "1":
                statue_dict = {"filename": filename, "statue": -1, "msg": u"文件正在更新"}
                statue_list.append(statue_dict)
                continue
            elif get_update_file_statue(filename) == "-1":
                statue_dict = {"filename": filename, "statue": -1, "msg": u"文件更新异常,点击异常查看异常信息"}
                statue_list.append(statue_dict)
                continue
            else:
                pass
            if filename.endswith(".xls") or filename.endswith(".xlsx"):
                file_statue = get_update_file_statue(filename)
                if file_statue == "2":
                    statue_dict= {"filename":filename, "statue":-2, "msg":u"文件已经更新了!"}
                else:
                    try:
                        file_path = UploadFileRecorde.objects.filter(filename=filename)[0].file_path
                        datas = read_xls(file_path)
                        update_file_statue(filename,1)
                        try:
                            import_one_file_to_statement_view.delay({"datas":datas,"filename":filename})
                            statue_dict = {"filename": filename, "statue": 0, "msg": ""}
                        except Exception, e:
                            print e
                            statue_dict = {"filename": filename, "statue": 0, "msg": str(e)}
                            update_file_statue(filename, -1, error_msg=str(e))
                        # statue_dict = {"filename": filename, "statue": statue.get("statue"), "msg": statue.get("msg","")}
                    except Exception, e:
                        statue_dict = {"filename": filename, "statue":-1, "msg": str(e)}
            else:
                print "not found .xls file"
                statue_dict = {"filename": filename, "statue": -1, "msg": u"文件不是.xls或.xlsx文件"}
            statue_list.append(statue_dict)
        return statue_list


def get_update_error_str(uid):
    try:
        error_msg = UploadFileRecorde.objects.filter(id=uid).values_list("error_msg", flat=True)[0]
    except Exception,e:
        print str(e)
        error_msg = u"没有找到这条记录!"
    return error_msg