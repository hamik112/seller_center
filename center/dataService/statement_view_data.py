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

# from manageApp.dataService.upload_file import get_path
from center.dataService.create_xls import generate_path
from manageApp.models import FilenameToStorename


GenerateReport_PATH = settings.GENERATE_REPORT_PATH



class StatementViewData(object):
    def __init__(self, username, post_dict, return_dict):
        self.username = username
        self.return_dict = return_dict
        self.post_dict = post_dict if post_dict else {}
        self.reportType = self.post_dict.get("reportType")
        self.timeRangeType = self.post_dict.get("timeRangeType", "")
        # print reportType, year, timeRangeType, month
        if self.timeRangeType == "Monthly" :
            self.year = self.post_dict.get("year")
            self.month = self.post_dict.get("month", "")
            self.current_month = self.get_month_day(self.year, self.month)
            self.is_custom = "Monthly"
            self.begin_date_str = str(self.current_month.get("day_begin", ""))
            self.end_date_str =  str(self.current_month.get("day_end", ""))
            self.timeRange = str(self.current_month.get("day_begin", "")) +" - "+ str(self.current_month.get("day_end", ""))
        elif self.timeRangeType == "Custom" :
            self.is_custom = "Custom"
            self.startDateYear = self.post_dict.get("startDate[year]", "")
            self.startDateMonth = self.post_dict.get("startDate[month]", "")
            self.startDateDay   = self.post_dict.get("startDate[date]", "")
            self.endDateYear    = self.post_dict.get("endDate[year]", "")
            self.endDateMonth   = self.post_dict.get("endDate[month]", "")
            self.endDateDay     = self.post_dict.get("endDate[date]", "")

            # self.startDateYear = self.post_dict.get("startDateYear","")
            # self.endDateYear = self.post_dict.get("endDateYear", "")
            # self.startDateMonth = self.post_dict.get("startDateMonth", "")
            # self.endDateMonth = self.post_dict.get("endDateMonth", "")
            # self.startDateDay = self.post_dict.get("startDateDay", "")
            # self.endDateDay = self.post_dict.get("endDateDay", "")
            self.begin_date_str = "%s %s, %s"%(self.startDateMonth, self.startDateDay, self.startDateYear)
            self.end_date_str = "%s %s, %s"%(self.endDateMonth, self.endDateDay, self.endDateYear)
            start_dateArray = datetime.datetime.strptime(self.begin_date_str, "%m %d, %Y")
            end_dateArray = datetime.datetime.strptime(self.end_date_str, "%m %d, %Y")
            self.begin_date_str = datetime.datetime.strftime(start_dateArray, "%b %d, %Y")
            self.end_date_str = datetime.datetime.strftime(end_dateArray, "%b %d, %Y")
            self.year = self.endDateYear
            self.month = self.endDateMonth
            self.timeRange = str(self.begin_date_str) + " - " + str(self.end_date_str)
        else:
            self.timeRange = ""
            self.current_month = {}
        pass

    def statement_data_read(self, **params):
        try:
            pageSize = int(params.get("pageSize", 10)) if int(params.get("pageSize", 10)) >= 10 else 10
            cur_page = int(params.get("cur_page", 1)) if int(params.get("cur_page", 1))>= 1 else 1
        except:
            pageSize, cur_page = 10, 1
        start_item = (cur_page - 1) * pageSize + 1
        username = self.username
        generate_report_list = GenerateReport.objects.filter(username=username).values().order_by("id").reverse()[pageSize * (cur_page -1): pageSize * cur_page + 1]
        # print generate_report_list
        return_report_list = []
        for fline in generate_report_list:
            if not os.path.exists(os.path.join(GenerateReport_PATH, fline.get("report_file_path",""))):
                fline["report_status"] = "1"
                return_report_list.append(fline)
            else:
                return_report_list.append(fline)
        if len(return_report_list) > 10:
            end_item = cur_page * pageSize
        else:
            end_item = start_item-1 + len(return_report_list)
        total_count = GenerateReport.objects.filter(username=self.username).count()
        if total_count % pageSize != 0:
            total_page = total_count / pageSize + 1
        else:
            total_page = total_count / pageSize
        if total_page > cur_page:
            next_page =  cur_page + 1
        else:
            next_page = total_page
        return {"recorde_list":return_report_list, "start_item":start_item, "total_count": total_count,
                "end_item":end_item, "total_page": total_page, "next_page":next_page}

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
            #return_dict = self.write_recorde_generate_report()
            return_dict = self.return_dict
            result = self.web_html_to_pdf()
            if result.get("statue", False):
                action_statue = "0"
            else:
                action_statue = "-1"
            update_statue = self.update_recorde_generate_report_statue(return_dict.get("return_id"), result.get("file_path_name",""),action_statue=action_statue)
            return result
        elif self.reportType == "Transaction" and self.timeRangeType =="Custom":
            #return_dict = self.write_recorde_generate_report()
            return_dict = self.return_dict
            result = self.create_xls_reports(**return_dict)
            print "create xls report result:", result
            if result.get("statue", False):
                action_statue = "0"
            else:
                action_statue = "-1"
            update_statue = self.update_recorde_generate_report_statue(return_dict.get("return_id"), result.get("file_path_name",""), action_statue=action_statue)
            return {"status": update_statue, "message":""}
            pass

        elif self.reportType == "Transaction" and self.timeRangeType == "Monthly":   #导出表格
            #return_dict = self.write_recorde_generate_report()
            return_dict = self.return_dict
            result = self.create_xls_reports(**return_dict)
            if result.get("statue", False):
                action_statue = "0"
            else:
                action_statue = "-1"
            update_statue = self.update_recorde_generate_report_statue(return_dict.get("return_id"), result.get("file_path_name",""), action_statue=action_statue)
            return {"status": update_statue, "message":""}
        else:
            return {"statusCode":"OK"}
        # statement_list = StatementView.objects.filter()




    def write_recorde_generate_report(self,action_statue=None):
        if not action_statue:
            action_statue = 0
        else:
            action_statue = action_statue
        username = self.username
        request_date = datetime.datetime.now().strftime("%b %m, %Y")
        recorde_dict = {"reportType": self.reportType, "year": self.year, "is_custom": self.is_custom, "timeRange": self.timeRange,
                        "timeRangeType": self.timeRangeType, "month": self.month, "action_statue": action_statue,"request_date":request_date,
                        "username":username}
        return_id = -1
        print "recorde_dict: ", recorde_dict
        gr = GenerateReport(**recorde_dict)
        try:
            gr.save()
            return_id = gr.id
        except Exception, e:
            print "Error, ",str(e)
        return {"return_id":return_id, "year": self.year, "month":self.month,
                "timeRange":self.timeRange}


    def update_recorde_generate_report_statue(self, recorde_id, file_path_name, action_statue=None):
        """ 更新记录 """
        if not action_statue:
            action_statue = 1
        else:
            action_statue = action_statue
        statue = True
        if not os.path.exists(file_path_name):
            statue = False
            # return statue
        try:
            report_file_path = file_path_name.split("GENERATE_REPORT/")[1]
        except Exception, e:
            print "file_path_name:",file_path_name
            report_file_path = ""

        try:
            GenerateReport.objects.filter(id=recorde_id).update(action_statue=action_statue,report_file_path=report_file_path)
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
        user_email = self.username
        begin_day, end_day = self.timeRange.split("-")
        begin_day_list = str(begin_day).strip().replace(",", "").split(" ")
        end_day_list = str(end_day).strip().replace(",", "").split(" ")
        if self.timeRangeType == "Monthly":
            filename = str(begin_day_list[2])+str(begin_day_list[0])+"_MonthlySummary.pdf"
        else:
            filename = str(begin_day_list[2]) + str(begin_day_list[0]) + str(begin_day_list[1]) + "-" +\
                       str(end_day_list[2]) + str(end_day_list[0]) + str(end_day_list[1]) + "_CustomSummary.pdf"
        output_file_name = os.path.join(generate_path(GenerateReport_PATH), filename)
        # options = {"year":self.year, "month":self.month,"begin_date":self.}
        try:
            serial_number = FilenameToStorename.objects.get(email=user_email).serial_number
        except Exception, e:
            msg = str(e)
            print msg
            statue = False
            return {"statue": statue, "msg": msg, "file_path_name": output_file_name}
        params = {"username":self.username,"month":self.month,"year":self.year,
                  "begin_date_str":str(self.begin_date_str),
                  "end_date_str": str(self.end_date_str),
                  "filename":output_file_name}
        try:
            print "params = " , params
            output_file_create = create_pdf_from_html(**params)
        except Exception, e:
            print "html to pdf error: ", str(e)
            output_file_create = ""
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
        begin_day_list = str(begin_day).strip().replace(",", "").split(" ")
        end_day_list = str(end_day).strip().replace(",", "").split(" ")
        if self.timeRangeType == "Monthly":
            filename = str(begin_day_list[2])+str(begin_day_list[0])+"_MonthlyTransaction.csv"
        else:
            filename = str(begin_day_list[2]) + str(begin_day_list[0]) + str(begin_day_list[1]) + "-" +\
                       str(end_day_list[2]) + str(end_day_list[0]) + str(end_day_list[1]) + "_CustomTransaction.csv"
        print "filename: ", filename
        begin_date = datetime.datetime.strptime(begin_day.strip(), "%b %d, %Y")
        end_date    = datetime.datetime.strptime(end_day.strip(), "%b %d, %Y")
        file_end_date = end_date + datetime.timedelta(days=1)  #date_time__range不包含最后一天
        print begin_date, end_date
        statue, msg, file_path_name = True, "", ""
        user_email = self.username
        try:
            serial_number = FilenameToStorename.objects.get(email=user_email).serial_number
        except Exception, e:
            msg = str(e)
            print msg
            statue = False
            return {"statue": statue, "msg": msg, "file_path_name": file_path_name}
        all_datas = StatementView.objects.filter(serial_number=serial_number,
                                                 date_time__range=(begin_date, file_end_date)).values_list("date_time",
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
            file_path_name = os.path.join(generate_path(GenerateReport_PATH), filename)
            filename = create_csv(**{"datas":all_datas, "header": header, "filename":file_path_name})
            print filename
        except Exception, e:
            statue = False
            msg = "create csv Error: " + str(e)
            print "msg: ", msg
        # try:
        #     wb, filename = create_xls(**{"datas": all_datas, "header": header, "filename": filename})
        #     file_path_name = os.path.join(generate_path(GenerateReport_PATH), filename)
        #     wb.save(file_path_name)
        # except Exception,e:
        #     statue = False
        #     msg = "create xls Error: " + str(e)
        #     print "msg: ", msg
        return  {"statue": statue, "msg": msg, "file_path_name": file_path_name}








