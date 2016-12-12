# encoding:utf-8
import  json
import  datetime

from django.http import StreamingHttpResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from center.dataService.statement_view_data import StatementViewData
from django.views.decorators.csrf import csrf_exempt

from django.contrib import  auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from center.dataService.data_format import file_iterator
from center.dataService.summary_pdf_data import SummaryPdfData, create_pdf_from_html
# Create your views here.


@login_required(login_url="/amazon-login/")
def home(request):
    return render(request, "Home.html", locals())

@login_required(login_url="/amazon-login/")
def inventory(request):
    return render(request, 'inventory.html', locals())

@login_required(login_url="/amazon-login/")
def pricing(request):
    return render(request, 'pricing.html', locals())

@login_required(login_url="/amazon-login/")
def orders(request):
    return render(request, 'orders.html', locals())

@login_required(login_url="/amazon-login/")
def advertising(request):
    return render(request, 'advertising-2.html', locals())

@login_required(login_url="/amazon-login/")
def performance(request):
    return render(request, 'performance.html', locals())

@login_required(login_url="/amazon-login/")
def transaction(request):
    return render(request, "transaction.html", locals())


@login_required(login_url="/amazon-login/")
def all_statements(request):
    return render(request, 'all_statements.html', locals())

@login_required(login_url="/amazon-login/")
@csrf_exempt
def date_range_reports(request):
    if request.method == "POST":
        print request.POST
        result = StatementViewData(request).request_report()
        print result
        return HttpResponse(json.dumps(result))
    else:
        recorde_list = StatementViewData(request).statement_data_read()
        # print recorde_list
        return  render(request, "data_range_reports.html", locals())

@login_required(login_url="/amazon-login/")
def statement_view(request):
    # result_dict = StatementViewData(request).test_return()
    return  render(request, 'statement_view.html', locals())








@login_required(login_url="/amazon-login/")
def download_file(request):
    file_type = request.GET.get("file_type", "octet-stream")    #vnd.ms-excel (.xls),  octet-stream(pdf) 下载文件
    file_name = request.GET.get("file_name", "not_found_file_name")
    if not file_name:
        return HttpResponseRedirect("/date-range-reports/")
    the_file_name = file_name.split("/")[-1]
    try:
        response = StreamingHttpResponse(file_iterator(file_name))
    except:
        return HttpResponseRedirect("/date-range-reports/")
    response['Content-Type'] = 'application/' + str(file_type)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response


@login_required(login_url="/amazon-login/")
def amazon_logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/amazon-login/")


def amazon_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        print email, password
        user = auth.authenticate(username=email, password=password)
        print user
        if user:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, 'amazon_login.html', locals())
    else:
        return render(request, 'amazon_login.html', locals())



def amazon_register(request):
    if request.method == "POST":
        username = request.POST.get("customerName", "")
        email = request.POST.get("email", "")
        password1 = request.POST.get("password", "")
        password2 = request.POST.get("passwordCheck", "")
        if not email or not username or not password1 or not password2:
            return render(request, 'amazon_register.html', locals())
        if password1 != password2:
            return render(request, 'amazon_register.html', locals())
        user = User()
        user.username = username
        user.email = email
        user.set_password(password1)
        try:
            user.save()
        except Exception,e:
            print e
            return render(request, 'amazon_register.html', locals())
        return HttpResponseRedirect("/amazon-login/")
    else:
        return render(request, 'amazon_register.html', locals())

