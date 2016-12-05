#/usr/bin/env python
# encoding:utf8

import  os
import  datetime
import calendar
import time

from django.conf import settings

from manageApp.models import StatementView

from  center.dataService.create_xls import create_xls
from center.models import  GenerateReport

from manageApp.dataService.upload_file import get_path



GenerateReport_PATH = settings.GENERATE_REPORT_PATH

class StatementViewData(object):
    def __init__(self, request):
        self.request =  request
        self.post_dict = request.POST if request.POST else {}
        pass

    def statement_data_read(self):
        generate_report_list = GenerateReport.objects.filter()
        return list(generate_report_list.values())

    def request_report(self):
        if self.post_dict.get("reportType", "") == "Summary":    # 导出pdf
            cur_path = self.request.get_host()
            pdf_url = "http://" + cur_path + "/summary-pdf/"
            date = datetime.datetime.now()
            datestr = date.strftime("%Y-%m-%d")
            return_id = self.write_recorde_generate_report()
            result = self.web_html_to_pdf(pdf_url, datestr+"_output.pdf")
            update_statue = self.update_recorde_generate_report_statue(return_id, result.get("file_path_name",""))
            return result
        elif self.post_dict.get("reportType", "") == "Transaction":   #导出表格
            return_id = self.write_recorde_generate_report()
            result = self.create_xls_reports()
            update_statue = self.update_recorde_generate_report_statue(return_id, result.get("file_path_name",""))
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
        reportType = self.post_dict.get("reportType")
        year = self.post_dict.get("year")
        timeRangeType = self.post_dict.get("timeRangeType")
        month = self.post_dict.get("month", "")
        print reportType, year, timeRangeType, month
        if timeRangeType == "Monthly":
            current_month = self.get_current_month_day()
            timeRange = str(current_month.get("day_begin", "")) +" - "+ str(current_month.get("day_end", ""))
        else:
            timeRange = ""
        request_date = datetime.datetime.now().strftime("%a %m, %Y")
        recorde_dict = {"reportType": reportType, "year": year, "is_custom": "Custom", "timeRange": timeRange,
                        "timeRangeType": timeRangeType, "month": month, "action_statue": 0,"request_date":request_date}
        return_id = -1
        print "recorde_dict: ", recorde_dict
        gr = GenerateReport(**recorde_dict)
        try:
            gr.save()
            return_id = gr.id
        except Exception, e:
            print "Error, ",str(e)
        return return_id


    def update_recorde_generate_report_statue(self, recorde_id, file_path_name):
        try:
            report_file_path = file_path_name.split("GENERATE_REPORT/")[1]
        except Exception, e:
            print "file_path_name:",file_path_name
            report_file_path = ""
        statue = True
        try:
            GenerateReport.objects.filter(id=recorde_id).update(action_statue=1,report_file_path=report_file_path)
        except Exception, e:
            print str(e)
            statue = False
        return statue

    def get_current_month_day(self):
        day_now = time.localtime()
        begin_day = 1
        wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
        end_day = monthRange
        mon_year = str(datetime.datetime.now().strftime("%a--%Y"))
        month, year = mon_year.split("--")
        begin_day = str(month) + " 1, "+ str(year)
        end_day = str(month) + " "+str(monthRange) +", "+str(year)
        return  {"day_begin": begin_day, "day_end": end_day}


    def web_html_to_pdf(self, url, output_file):
        statue, msg, output_file_name = True, "", ""
        output_file_name = os.path.join(get_path(GenerateReport_PATH), output_file)
        try:
            os.system("wkhtmltopdf " + url+ " " + output_file_name)
        except Exception, e:
            print "html to pdf error: ", str(e)
            statue = False
        return {"statue": statue, "msg": msg, "file_path_name": output_file_name}


    def create_xls_reports(self):
        statue, msg, file_path_name = True, "", ""
        all_datas = StatementView.objects.filter().values_list("settlement_id", "type", "order_id", "sku", "description",
                  "quantity", "marketplace", "fulfillment", "order_city",
                  "order_state", "order_postal", "product_sales", "shipping_credits",
                  "promotional_rebates", "sales_tax_collected", "selling_fees",
                  "fba_fees", "other_transaction_fees", "other", "total", "store_name")

        header = ["settlement id", "type", "order id", "sku", "description",
                  "quantity", "marketplace", "fulfillment", "order city",
                  "order state", "order postal", "product sales", "shipping credits",
                  "promotional rebates", "sales tax collected", "selling fees",
                  "fba fees", "other transaction fees", "other", "total", u"店铺名"]
        try:
            wb, filename = create_xls(**{"datas": all_datas, "header": header})
            file_path_name = os.path.join(get_path(GenerateReport_PATH), filename)
            wb.save(file_path_name)
        except Exception,e:
            statue = False
            msg = "create xls Error: " + str(e)
        return  {"statue": statue, "msg": msg, "file_path_name": file_path_name}







