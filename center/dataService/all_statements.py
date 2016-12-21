#!/usr/bin/env python
# encoding:utf-8

from django.conf import  settings

from center.models import  AllStatements
from center.dataService.create_xls import is_number


def number_format(num):
    if num != 0:
        num = str("%.2f"%float(num))
    else:
        num = 0
    if float(num) >= 1000 or float(num) <= -1000:
        num = format(float(num),",")
    return str(num)



class AllStatementsList(object):
    def __init__(self, username):
        self.username = username
        pass

    def get_all_statements_file(self):
        try:
            all_statements_list = AllStatements.objects.filter(username=self.username).values("settlement_period",
            "beginning_balance","product_charges_total", "promo_retates_total", "amazon_fees_total", "other_total",
            "deposit_total","filename")
        except Exception,e :
            all_statements_list = []
        all_statements_list = self.dear_list(all_statements_list)
        return all_statements_list


    def dear_list(self,file_list):
        return_list = []
        for lst in file_list:
            tmp_dict = {}
            for k,v in lst.iteritems():
                if is_number(v):
                    tmp_dict[k]=self.number_add_dot(v)
                else:
                    tmp_dict[k] = v
            return_list.append(tmp_dict)
        return return_list

    def number_add_dot(self,num):
        if float(num) < 0:
            num = number_format(num)
            return "-$"+str(num).replace("-","")
        else:
            num = number_format(num)
            return "$"+str(num)