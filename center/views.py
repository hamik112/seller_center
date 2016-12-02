# encoding:utf-8
import  json


from django.shortcuts import render, HttpResponse
from center.dataService.statement_view_data import StatementViewData
from django.views.decorators.csrf import csrf_exempt

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



