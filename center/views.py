# encoding:utf-8
import  json

from django.http import StreamingHttpResponse
from django.shortcuts import render, HttpResponse
from center.dataService.statement_view_data import StatementViewData
from django.views.decorators.csrf import csrf_exempt

from center.dataService.data_format import file_iterator
# Create your views here.


def home(request):
    return render(request, "Home.html", locals())


def inventory(request):
    return render(request, 'inventory.html', locals())


def pricing(request):

    return render(request, 'pricing.html', locals())


def orders(request):
    return render(request, 'orders.html', locals())


def advertising(request):

    return render(request, 'advertising-2.html', locals())

def performance(request):

    return render(request, 'performance.html', locals())

def transaction(request):
    return render(request, "transaction.html", locals())



def all_statements(request):
    return render(request, 'all_statements.html', locals())


@csrf_exempt
def date_range_reports(request):
    if request.method == "POST":
        print request.POST
        result = StatementViewData(request).request_report()
        return HttpResponse(json.dumps(result))
    else:
        recorde_list = StatementViewData(request).statement_data_read()
        print recorde_list
        return  render(request, "data_range_reports.html", locals())


def statement_view(request):
    result_dict = StatementViewData(request).test_return()
    return  render(request, 'statement_view.html', locals())




def pdf_file_view(request):
    return render(request, "pdf_hml/2016Jun_MonthlySummary.html", locals())






def download_file(request):
    file_type = request.GET.get("file_type", "octet-stream")    #vnd.ms-excel (.xls),  octet-stream(pdf) 下载文件
    file_name = request.GET.get("file_name", "not_found_file_name")
    the_file_name = file_name.split("/")[-1]
    response = StreamingHttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/' + str(file_type)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response



