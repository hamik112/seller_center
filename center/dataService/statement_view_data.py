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



UPLOAD_PATH = settings.UPLOAD_PATH

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
            update_statue = self.update_recorde_generate_report_statue(return_id)
            return result
        elif self.post_dict.get("reportType", "") == "Transaction":   #导出表格
            return_id = self.write_recorde_generate_report()
            result = self.create_xls_reports()
            update_statue = self.update_recorde_generate_report_statue(return_id)
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
        if timeRangeType == "Monthly":
            current_month = self.get_current_month_day()
            timeRange = str(current_month.get("day_begin", "")) + str(current_month.get("day_end", ""))
        else:
            timeRange = ""
        recorde_dict = {"reportType": reportType, "year": year, "is_custom": "custom", "timeRange": timeRange,
                        "timeRangeType": timeRangeType, "month": month, "action_statue": 0}
        return_id = -1
        print "recorde_dict: ", recorde_dict
        gr = GenerateReport(**recorde_dict)
        try:
            gr.save()
            return_id = gr.id
        except Exception, e:
            print "Error, ",str(e)
        return return_id

    def update_recorde_generate_report_statue(self, recorde_id):
        statue = True
        try:
            GenerateReport.objects.filter(id=recorde_id).update(action_statue=1)
        except Exception, e:
            print str(e)
            statue = False
        return statue

    def get_current_month_day(self):
        day_now = time.localtime()
        day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
        wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
        day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
        return  {"day_begin": day_begin, "day_end": day_end}


    def web_html_to_pdf(self, url, output_file):
        statue, msg = True, ""
        upload_path = settings.UPLOAD_PATH
        output_file_name = os.path.join(upload_path, output_file)
        try:
            os.system("wkhtmltopdf " + url+ " " + output_file_name)
        except Exception, e:
            print "html to pdf error: ", str(e)
            statue = False
        return {"statue": statue, "msg": msg}


    def create_xls_reports(self):
        statue, msg = True, ""
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
            file_path_name = os.path.join(UPLOAD_PATH, filename)
            wb.save(file_path_name)
        except Exception,e:
            statue = False
            msg = "create xls Error: " + str(e)
        return  {"statue": statue, "msg": msg}







