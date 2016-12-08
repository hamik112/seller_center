#!/usr/bin/env python
# encoding:utf-8

from django.db.models import  Sum

from manageApp.models import StatementView
from manageApp.models import FilenameToStorename



def pdf_number_len(number_str):
    # y = -0.278x + 31.97  --> x 为 product_sale_sum 的长度， 即: len(product_sale_sum)
    x = len(number_str)
    return -0.278 * x + 31.97



class SummaryPdfData(object):
    def __init__(self, username, **params):
        self.username = username
        self.year = params.get("year", "")
        self.month = params.get("month", "")
        self.begin_date = params.get("begin_date", "")
        self.end_date = params.get("end_date", "")
        self.serial_number = self.get_serial_number()

    def get_serial_number(self):
        try:
            serial_number = FilenameToStorename.objects.filter(email=self.username).values_list("serial_number", flat=True)[0]
        except Exception, e:
            serial_number = ""
        return serial_number

    def get_storename(self):
        try:
            storename = FilenameToStorename.objects.filter(serial_number=self.serial_number).values_list("storename", flat=True)[0]
        except Exception, e:
            print str(e)
            storename = ""
        return storename

    def product_sales(self):
        print self.serial_number
        try:
            product_sale_query_dict = StatementView.objects.filter(serial_number=self.serial_number,
                                                        type="Order",
                                                        fulfillment="Amazon").values("product_sales", "other").aggregate(Sum("product_sales"),Sum("other"))
        except Exception, e:
            product_sale_query_dict = {}
        if product_sale_query_dict.get("product_sales__sum") and product_sale_query_dict.get("other__sum"):
            product_sale_sum = product_sale_query_dict.get("product_sales__sum", 0) + product_sale_query_dict.get("other__sum", 0)
        else:
            product_sale_sum = 0
        product_sale_sum = format(product_sale_sum, ",")
        product_sale_html_sum = pdf_number_len(product_sale_sum)
        return {"number_length": product_sale_html_sum, "number": product_sale_sum}



    def get_pdf_data(self,**params):

        pass