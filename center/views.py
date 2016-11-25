# encoding:utf-8
from django.shortcuts import render

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


def date_range_reports(request):
    return  render(request, "data_range_reports.html", locals())


def statement_view(request):
    return  render(request, 'statement_view.html', locals())