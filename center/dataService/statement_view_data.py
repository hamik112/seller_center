#/usr/bin/env python
# encoding:utf8

import  os
import  datetime
import calendar
import time
import  urllib
import  pdfkit

from django.conf import settings

from manageApp.models import StatementView

from  center.dataService.create_xls import create_xls
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
        generate_report_list = GenerateReport.objects.filter()
        return_report_list = []
        for fline in generate_report_list.values():
            if not os.path.exists(os.path.join(GenerateReport_PATH, fline.get("report_file_path",""))):
                continue
            else:
                return_report_list.append(fline)
        return return_report_list

    def request_report(self):
        if self.post_dict.get("reportType", "") == "Summary":    # 导出pdf
            cur_path = self.request.get_host()
            pdf_url = "http://" + cur_path + "/summary-pdf/?"
            pdf_url  +=  "year="+self.year+"&month="+self.month + \
                       "&begin_date="+str(self.current_month.get("day_begin", "")) + \
                       "&end_date="+  str(self.current_month.get("day_end", ""))
            pdf_url = pdf_url.replace(" ", "%20").replace(",","%2c")
            print pdf_url
            date = datetime.datetime.now()
            datestr = date.strftime("%Y-%m-%d")
            return_dict = self.write_recorde_generate_report()
            result = self.web_html_to_pdf(pdf_url, datestr+"_output.pdf")
            update_statue = self.update_recorde_generate_report_statue(return_dict.get("return_id"), result.get("file_path_name",""))
            return result
        elif self.post_dict.get("reportType", "") == "Transaction":   #导出表格
            return_dict = self.write_recorde_generate_report()
            result = self.create_xls_reports(**return_dict)
            update_statue = self.update_recorde_generate_report_statue(return_dict.get("return_id"), result.get("file_path_name",""))
            return update_statue
        # statement_list = StatementView.objects.filter()



    def test_return(self):
        return {"unsuccessful_charges": "57",
                "seller_repayment": "37.7",
                "seller_repayment_subtotal": "37.7",
                "product_charges": "0.1",
                "promo_rebates": "0.2",
                "amazon_fees": "0.3",
                "other": "0.4",
                "other_subtotal": "0.5",
                "product_charges": "0.6",
                "product_charges_subtotal": "0.7"
                }


    def write_recorde_generate_report(self):

        request_date = datetime.datetime.now().strftime("%b %m, %Y")
        recorde_dict = {"reportType": self.reportType, "year": self.year, "is_custom": "Custom", "timeRange": self.timeRange,
                        "timeRangeType": self.timeRangeType, "month": self.month, "action_statue": 0,"request_date":request_date}
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


    def web_html_to_pdf(self, url, output_file):
        statue, msg, output_file_name = True, "", ""
        output_file_name = os.path.join(get_path(GenerateReport_PATH), output_file)
        user_email = self.request.user.username
        # options = {"year":self.year, "month":self.month,"begin_date":self.}
        try:
            serial_number = FilenameToStorename.objects.get(email=user_email).serial_number
        except Exception, e:
            msg = str(e)
            print msg
            statue = False
            return {"statue": statue, "msg": msg, "file_path_name": output_file_name}
        try:
            config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
            pdfkit.from_url(url, output_file_name, configuration=config)
            # os.system("wkhtmltopdf " + url+ " " + output_file_name)
        except Exception, e:
            print "html to pdf error: ", str(e)
            statue = False
        return {"statue": statue, "msg": msg, "file_path_name": output_file_name}


    def create_xls_reports(self, **params):
        timeRange = params.get("timeRange", "")
        begin_day, end_day = timeRange.split("-")
        begin_date = datetime.datetime.strptime(begin_day.strip(), "%b %d, %Y")
        end_date    = datetime.datetime.strptime(end_day.strip(), "%b %d, %Y")
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
                  "order_state", "order_postal", "product_sales", "shipping_credits",
                  "promotional_rebates", "sales_tax_collected", "selling_fees",
                  "fba_fees", "other_transaction_fees", "other", "total")

        header = ["date/time","settlement id", "type", "order id", "sku", "description",
                  "quantity", "marketplace", "fulfillment", "order city",
                  "order state", "order postal", "product sales", "shipping credits",
                  "promotional rebates", "sales tax collected", "selling fees",
                  "fba fees", "other transaction fees", "other", "total"]
        print "all_data:", len(all_datas)
        try:
            wb, filename = create_xls(**{"datas": all_datas, "header": header})
            file_path_name = os.path.join(get_path(GenerateReport_PATH), filename)
            wb.save(file_path_name)
        except Exception,e:
            statue = False
            msg = "create xls Error: " + str(e)
            print "msg: ", msg
        return  {"statue": statue, "msg": msg, "file_path_name": file_path_name}








