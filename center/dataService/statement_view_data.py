#/usr/bin/env python
# encoding:utf8

import  os
import  datetime
import calendar
import time
import  urllib
# import  pdfkit

from django.conf import settings

from manageApp.models import StatementView

from  center.dataService.create_xls import create_xls, create_csv
from center.dataService.summary_pdf_data import create_pdf_from_html
from center.models import  GenerateReport

from manageApp.dataService.upload_file import get_path
from manageApp.models import FilenameToStorename


GenerateReport_PATH = settings.GENERATE_REPORT_PATH



class StatementViewData(object):
    def __init__(self, request):
        self.request =  request
        self.post_dict = request.POST if request.POST else {}
        self.reportType = self.post_dict.get("reportType")
        self.year = self.post_dict.get("year")
        self.timeRangeType = self.post_dict.get("timeRangeType", "")
        self.month = self.post_dict.get("month", "")
        # print reportType, year, timeRangeType, month
        if self.timeRangeType == "Monthly":
            self.current_month = self.get_month_day(self.year, self.month)
            self.timeRange = str(self.current_month.get("day_begin", "")) +" - "+ str(self.current_month.get("day_end", ""))
        else:
            self.timeRange = ""
            self.current_month = {}
        pass

    def statement_data_read(self):
        username = self.request.user.username
        generate_report_list = GenerateReport.objects.filter(username=username)
        return_report_list = []
        for fline in generate_report_list.values():
            if not os.path.exists(os.path.join(GenerateReport_PATH, fline.get("report_file_path",""))):
                continue
            else:
                return_report_list.append(fline)
        return return_report_list[::-1]

    def request_report(self):
        if self.post_dict.get("reportType", "") == "Summary":    # 导出pdf
            # cur_path = self.request.get_host()
            # pdf_url = "http://" + cur_path + "/summary-pdf/?"
            # pdf_url  +=  "year="+self.year+"&month="+self.month + \
            #            "&begin_date="+str(self.current_month.get("day_begin", "")) + \
            #            "&end_date="+  str(self.current_month.get("day_end", ""))
            # pdf_url = pdf_url.replace(" ", "%20").replace("&","\&").replace("%", "\%").replace(",", "\,")
            # print pdf_url
            # date = datetime.datetime.now()
            # datestr = date.strftime("%Y-%m-%d_%H-%M-%S")
            return_dict = self.write_recorde_generate_report()
            result = self.web_html_to_pdf()
            update_statue = self.update_recorde_generate_report_statue(return_dict.get("return_id"), result.get("file_path_name",""))
            return result
        elif self.post_dict.get("reportType", "") == "Transaction" :   #导出表格
            return_dict = self.write_recorde_generate_report()
            result = self.create_xls_reports(**return_dict)
            update_statue = self.update_recorde_generate_report_statue(return_dict.get("return_id"), result.get("file_path_name",""))
            return update_statue
        # statement_list = StatementView.objects.filter()




    def write_recorde_generate_report(self):
        username = self.request.user.username
        request_date = datetime.datetime.now().strftime("%b %m, %Y")
        recorde_dict = {"reportType": self.reportType, "year": self.year, "is_custom": "Custom", "timeRange": self.timeRange,
                        "timeRangeType": self.timeRangeType, "month": self.month, "action_statue": 0,"request_date":request_date,
                        "username":username}
        return_id = -1
        # print "recorde_dict: ", recorde_dict
        gr = GenerateReport(**recorde_dict)
        try:
            gr.save()
            return_id = gr.id
        except Exception, e:
            print "Error, ",str(e)
        return {"return_id":return_id, "year": self.year, "month":self.month,
                "timeRange":self.timeRange}


    def update_recorde_generate_report_statue(self, recorde_id, file_path_name):
        """ 更新记录 """
        statue = True
        if not os.path.exists(file_path_name):
            statue = False
            return statue
        try:
            report_file_path = file_path_name.split("GENERATE_REPORT/")[1]
        except Exception, e:
            print "file_path_name:",file_path_name
            report_file_path = ""

        try:
            GenerateReport.objects.filter(id=recorde_id).update(action_statue=1,report_file_path=report_file_path)
        except Exception, e:
            print str(e)
            statue = False
        return statue

    def get_month_day(self, num_year,num_month):
        wday, monthRange = calendar.monthrange(int(num_year), int(num_month))
        in_year = str(num_month) +"--"+ str(num_year)
        datetime_year = datetime.datetime.strptime(in_year, "%m--%Y")
        mon_year = str(datetime_year.strftime("%b--%Y"))
        month, year = mon_year.split("--")
        begin_day = str(month) + " 1, "+ str(year)
        end_day = str(month) + " "+str(monthRange) +", "+str(year)
        return  {"day_begin": begin_day, "day_end": end_day}


    def web_html_to_pdf(self):
        statue, msg, output_file_name = True, "", ""
        user_email = self.request.user.username
        begin_day, end_day = self.timeRange.split("-")
        begin_day_list = str(begin_day).replace(",", "").split(" ")
        end_day_list = str(end_day).replace(",", "").split(" ")
        if self.timeRangeType == "Monthly":
            filename = str(begin_day_list[2])+str(begin_day_list[0])+"_MonthlyTransaction.pdf"
        else:
            filename = str(begin_day_list[2]) + str(begin_day_list[0]) + str(begin_day_list[1]) + "-"
            + str(end_day_list[2]) + str(end_day_list[0]) + str(end_day_list[1]) + "_CustomTransaction.pdf"
        output_file_name = os.path.join(get_path(GenerateReport_PATH), filename)
        # options = {"year":self.year, "month":self.month,"begin_date":self.}
        try:
            serial_number = FilenameToStorename.objects.get(email=user_email).serial_number
        except Exception, e:
            msg = str(e)
            print msg
            statue = False
            return {"statue": statue, "msg": msg, "file_path_name": output_file_name}
        params = {"username":self.request.user.username,"month":self.month,"year":self.year,
                  "begin_date_str":str(self.current_month.get("day_begin", "")),
                  "end_date_str": str(self.current_month.get("day_end", "")),
                  "filename":output_file_name}
        try:
            output_file_create = create_pdf_from_html(**params)
        except Exception, e:
            print "html to pdf error: ", str(e)
            statue = False
        # try:
        #     filename = output_file_name.split(".")[0]
        #     output_file_name_png = filename + ".png"
        #     pdf_filename = filename + ".pdf"
        #     create_pdf_from_html()
        #
        #     print output_file_name, pdf_filename
        #     # bash_str = "wkhtmltoimage" +" " + url+ "  " + output_file_name_png
        #     bash_str = "wkhtmltopdf " + " " + url + " " + pdf_filename
        #     convert_img_pdf_bash_str = "convert" + " " + output_file_name_png + "  " + pdf_filename
        #     os.popen(bash_str)
        #     # os.system(convert_img_pdf_bash_str)
        #     # output_file_name = output_file_name_png
        #     output_file_name = pdf_filename
        # except Exception, e:
        #     print "html to pdf error: ", str(e)
        #     statue = False
        return {"statue": statue, "msg": msg, "file_path_name": output_file_create}


    def create_xls_reports(self, **params):
        timeRange = params.get("timeRange", "")
        begin_day, end_day = timeRange.split("-")
        print "timeRange:", begin_day, end_day
        begin_day_list = str(begin_day).replace(",", "").split(" ")
        end_day_list = str(end_day).replace(",", "").split(" ")
        if self.timeRangeType == "Monthly":
            filename = str(begin_day_list[2])+str(begin_day_list[0])+"_MonthlyTransaction.csv"
        else:
            filename = str(begin_day_list[2]) + str(begin_day_list[0]) + str(begin_day_list[1]) + "-"
            + str(end_day_list[2]) + str(end_day_list[0]) + str(end_day_list[1]) + "_CustomTransaction.csv"
        print "filename: ", filename
        begin_date = datetime.datetime.strptime(begin_day.strip(), "%b %d, %Y")
        end_date    = datetime.datetime.strptime(end_day.strip(), "%b %d, %Y") + datetime.timedelta(days=1)  #date_time__range不包含最后一天
        print begin_date, end_date
        statue, msg, file_path_name = True, "", ""
        user_email = self.request.user.username
        try:
            serial_number = FilenameToStorename.objects.get(email=user_email).serial_number
        except Exception, e:
            msg = str(e)
            print msg
            statue = False
            return {"statue": statue, "msg": msg, "file_path_name": file_path_name}
        all_datas = StatementView.objects.filter(serial_number=serial_number,
                                                 date_time__range=(begin_date, end_date)).values_list("date_time",
                 "settlement_id", "type", "order_id", "sku", "description",
                  "quantity", "marketplace", "fulfillment", "order_city",
                  "order_state", "order_postal", "product_sales", "shipping_credits","gift_wrap_credits",
                  "promotional_rebates", "sales_tax_collected", "selling_fees",
                  "fba_fees", "other_transaction_fees", "other", "total")

        header = ["date/time","settlement id", "type", "order id", "sku", "description",
                  "quantity", "marketplace", "fulfillment", "order city",
                  "order state", "order postal", "product sales", "shipping credits","gift wrap credits",
                  "promotional rebates", "sales tax collected", "selling fees",
                  "fba fees", "other transaction fees", "other", "total"]
        print "all_data:", len(all_datas)
        try:
            file_path_name = os.path.join(get_path(GenerateReport_PATH), filename)
            filename = create_csv(**{"datas":all_datas, "header": header, "filename":file_path_name})
        except Exception, e:
            statue = False
            msg = "create csv Error: " + str(e)
            print "msg: ", msg
        # try:
        #     wb, filename = create_xls(**{"datas": all_datas, "header": header, "filename": filename})
        #     file_path_name = os.path.join(get_path(GenerateReport_PATH), filename)
        #     wb.save(file_path_name)
        # except Exception,e:
        #     statue = False
        #     msg = "create xls Error: " + str(e)
        #     print "msg: ", msg
        return  {"statue": statue, "msg": msg, "file_path_name": file_path_name}








