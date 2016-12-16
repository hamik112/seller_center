#!/usr/bin/env python
# encoding:utf-8

import  os
import  datetime
from django.db.models import  Q

# from django.contrib.auth.models import User
from django.conf import  settings

from manageApp.models import StatementView, FilenameToStorename
from center.dataService.create_xls import generate_path, create_txt
from center.dataService.create_xls import datetime_to_str_2, str_to_datetime






generate_report_path = settings.GENERATE_REPORT_PATH



class TrasactionView(object):
    def __init__(self, username, params):
        self.username = username
        self.subview = params.get("subview", "")
        self.post_dict = params
        print params
        self.query_select, self.serial_number = self.get_query_select()
        try:
            self.pageSize = int(params.get("pageSize", 10)) if int(params.get("pageSize", 10)) >= 10 else 10
            self.cur_page = int(params.get("cur_page", 1)) if int(params.get("cur_page", 1))>= 1 else 1
        except:
            self.pageSize, self.cur_page = 10, 1
        pass

    def get_query_select(self):
        start_date, end_date = self.get_time_range()
        print "start_date:", start_date, "end_date:", end_date
        try:
            serial_number = FilenameToStorename.objects.get(email=self.username).get_serial_number()
        except Exception, e:
            serial_number = ""
        query_select = Q(serial_number=serial_number)
        if start_date and end_date:
            query_select = query_select & Q(date_time__range=(start_date,end_date))
        order_type = self.post_dict.get("eventType", "").strip()
        print "order_type: ", order_type
        if order_type == "selected":
            query_select = query_select
        else:
            query_select = query_select & Q(type=order_type)
        return  query_select, serial_number


    def get_time_range(self):
        time_range_list = self.post_dict.get("groupId", "").split("-")
        if len(time_range_list) <= 0:
            time_range_list = ["" , ""]
        start_date = str_to_datetime(time_range_list[0].strip())
        end_date = str_to_datetime(time_range_list[1].strip())
        return start_date, end_date

    def get_transaction_view(self):
        if self.subview == "groups":
            return self.groups_view()
        else:
            return {"recorde_list": [], "start_item": 0, "end_item": 0, "total_page": 1, "next_page": 1}

    def groups_view(self):
        groupId = self.post_dict.get("groupId", "")
        cur_page, pageSize  = self.cur_page, self.pageSize
        start_item = (self.cur_page - 1) * self.pageSize
        query_select = self.query_select
        print "query_select: ", query_select, self.serial_number
        if not self.serial_number:
            return {"recorde_list":[], "start_item":0,"end_item":0, "total_page": 1, "next_page":1}
        groups_list = StatementView.objects.filter(query_select).values()[pageSize * (cur_page -1): pageSize * cur_page + 1]

        start_item = 0 if start_item == 0 and not groups_list else start_item + 1
        if len(groups_list) > 10:
            end_item = cur_page * pageSize
        else:
            end_item = 0 if start_item <= 0 else start_item - 1 + len(groups_list)
        total_count = StatementView.objects.filter(query_select).count()
        if total_count % pageSize != 0:
            total_page = total_count / pageSize + 1
        else:
            total_page = total_count / pageSize
        if total_page > cur_page:
            next_page =  cur_page + 1
        else:
            next_page = total_page
        for line in groups_list:
            line["date_time"] = datetime_to_str_2(line.get("date_time"))
            line["amazon_fees"] = "%.2f" %(float(line.get("fba_fees", 0.00)) + float(line.get("selling_fees", 0.00)))
            line["product_sales"] = '%.2f' % float(line.get("product_sales"))
            # print line.get("product_sales"), line.get("id")
            line["promotional_rebates"] = '%.2f' % float(line.get("promotional_rebates"))
            line["other"] = '%.2f' % float(line.get("other"))

        return {"recorde_list":groups_list[::-1], "start_item":start_item,
                "end_item":end_item, "total_page": total_page, "next_page":next_page}



    def write_report_to_txt(self):
        groupId = self.post_dict.get("groupId", "")
        pageSize  = self.pageSize
        print "pageSize: ", pageSize
        query_select = self.query_select
        if not self.serial_number:
            groups_list = []
        else:
            try:
                groups_list = StatementView.objects.filter(query_select).values_list("date_time", "order_id","sku",
                                                                                 "type", "description",  "total","quantity")[0: 600]
            except Exception, e:
                groups_list = []
        header_list = ["Transaction Summary for December 7, 2016 to December 15, 2016", "Transactions: 10", "",
                       "Date	Order ID	SKU	Transaction type	Payment Type	Payment Detail	Amount	Quantity	Product Title"]
        file_path_name = os.path.join(generate_path(generate_report_path), "report.txt")
        filename = create_txt(**{"header": header_list, "datas": groups_list, "filename":file_path_name})
        return filename





