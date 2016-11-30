#!/usr/bin/env python
# encoding:utf-8


from manageApp.dataService.deal_xls import read_xls
from manageApp.models import StatementView


class StatementViewImport(object):
    def __init__(self, files_list):
        self.files_list = files_list

    def import_files_to_statement_view(self):
        for filename in self.files_list:
            if filename.endswith(".xls") or filename.endswith(".xlsx"):
                datas = read_xls(filename)
            else:
                print "not found .xls file"
        pass

    def import_one_file_to_statement_view(self, datas):
        print datas

        return True


