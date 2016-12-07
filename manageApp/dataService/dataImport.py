#!/usr/bin/env python
# encoding:utf-8

import  datetime
import threading



from manageApp.dataService.deal_xls import read_xls
from manageApp.models import StatementView, UploadFileRecorde

from manageApp.tasks import import_one_file_to_statement_view
from manageApp.dataService.tasks_util import update_file_statue


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
                    datas = read_xls(file_path)
                    update_file_statue(filename,1)
                    # statue = self.import_one_file_to_statement_view(datas, filename)
                    # t = threading.Thread(target=self.import_one_file_to_statement_view, args=(datas, filename))
                    # t.start()
                    import_one_file_to_statement_view.delay({"datas":datas,"filename":filename})
                    statue_dict = {"filename": filename, "statue": 0, "msg": ""}
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