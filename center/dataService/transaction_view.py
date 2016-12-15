#!/usr/bin/env python
# encoding:utf-8

from django.db.models import  Q

# from django.contrib.auth.models import User


from manageApp.models import StatementView, FilenameToStorename



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
        try:
            serial_number = FilenameToStorename.objects.get(email=self.username).get_serial_number()
        except Exception, e:
            serial_number = ""
        query_select = Q(serial_number=serial_number)
        order_type = self.post_dict.get("eventType", "").strip()
        print "order_type: ", order_type
        if order_type == "selected":
            query_select = query_select
        else:
            query_select = query_select & Q(type=order_type)
        return  query_select, serial_number

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
            line["date_time"] = date_time_to_str(line.get("date_time"))
            line["amazon_fees"] = "%.2f" %(float(line.get("fba_fees", 0.00)) + float(line.get("selling_fees", 0.00)))
            line["product_sales"] = '%.2f' % float(line.get("product_sales"))
            print line.get("product_sales"), line.get("id")
            line["promotional_rebates"] = '%.2f' % float(line.get("promotional_rebates"))
            line["other"] = '%.2f' % float(line.get("other"))

        return {"recorde_list":groups_list[::-1], "start_item":start_item,
                "end_item":end_item, "total_page": total_page, "next_page":next_page}




def date_time_to_str(dt):
    return dt.strftime("%b %d, %Y")  # PDT, PST
