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
from center.dataService.get_storename import get_storename
from center.dataService.summary_pdf_data import SummaryPdfData
from center.dataService.transaction_view import TrasactionView

# Create your views here.


@login_required(login_url="/amazon-login/")
def home(request):
    email = request.user.username
    store_name = get_storename(email)
    return render(request, "Home.html", locals())

@login_required(login_url="/amazon-login/")
def inventory(request):
    email = request.user.username
    store_name = get_storename(email)
    return render(request, 'inventory.html', locals())

@login_required(login_url="/amazon-login/")
def pricing(request):
    email = request.user.username
    store_name = get_storename(email)
    return render(request, 'pricing.html', locals())

@login_required(login_url="/amazon-login/")
def orders(request):
    email = request.user.username
    store_name = get_storename(email)
    return render(request, 'orders.html', locals())

@login_required(login_url="/amazon-login/")
def advertising(request):
    email = request.user.username
    store_name = get_storename(email)
    return render(request, 'advertising-2.html', locals())

@login_required(login_url="/amazon-login/")
def performance(request):
    email = request.user.username
    store_name = get_storename(email)
    return render(request, 'performance.html', locals())

@login_required(login_url="/amazon-login/")
def transaction(request):
    username = request.user.username
    store_name = get_storename(username)
    return render(request, "transaction.html", locals())


@login_required(login_url="/amazon-login/")
def transaction_data(request):
    username = request.user.username
    store_name = get_storename(username)
    cur_page = int(request.GET.get("cur_page", 1))
    pageSize = request.GET.get("pageSize", 10)
    pageSize = 10 if pageSize == 10 or pageSize == "10" or pageSize == "Ten" else 10
    eventType  = request.GET.get("eventType","")
    mostRecentLast = request.GET.get("mostRecentLast","0")
    Update  =  request.GET.get("Update", "")
    subview = request.GET.get("subview", "")
    groupId = request.GET.get("groupdId", "")
    view = request.GET.get("view", "")
    recorde_result = TrasactionView(username,request.GET).get_transaction_view()
    # print recorde_result
    recorde_list = recorde_result.get("recorde_list", [])
    start_item = recorde_result.get("start_item", 1)
    end_item = recorde_result.get("end_item", 1)
    total_page = recorde_result.get("total_page", 1)
    next_page = int(recorde_result.get("next_page", 1))
    total_page_list = range(1, total_page + 1)
    pre_page = 0 if cur_page  <= 0 else int(cur_page) - 1
    return render(request, "transaction.html", locals())


#ict: {u'pageSize': [u'Ten'], u'eventType': [u'Refund'], u'mostRecentLast': [u'0'], u'Update': [u''], u'subview': [u'groups'], u'searchLanguage': [u'en_US'], u'groupId': [u'2016290Df-4nXYET2mOMsbCKQkt8Q'], u'view': [u'filter']}>








@login_required(login_url="/amazon-login/")
def all_statements(request):
    email = request.user.username
    store_name = get_storename(email)
    return render(request, 'all_statements.html', locals())

@login_required(login_url="/amazon-login/")
@csrf_exempt
def date_range_reports(request):
    email = request.user.username
    store_name = get_storename(email)
    if request.method == "POST":
        # print request.POST
        result = StatementViewData(request).request_report()
        # print result
        return HttpResponse(json.dumps(result))
    else:
        pageSize = request.GET.get("pageSize",10)
        cur_page = request.GET.get("cur_page",1)

        recorde_result = StatementViewData(request).statement_data_read(**{"pageSize":pageSize,"cur_page":cur_page})
        recorde_list = recorde_result.get("recorde_list", [])
        start_item = recorde_result.get("start_item",1)
        end_item   = recorde_result.get("end_item",1)
        total_page = recorde_result.get("total_page", 1)
        next_page = recorde_result.get("next_page", 1)
        total_page_list = range(1,total_page+1)
        if int(cur_page) < int(total_page):
            next = 1
        else:
            next = 0
        # print recorde_list
        return  render(request, "data_range_reports.html", locals())

@login_required(login_url="/amazon-login/")
def statement_view(request):
    email = request.user.username
    store_name = get_storename(email)
    # result_dict = StatementViewData(request).test_return()

    return  render(request, 'statement_view.html', locals())








@login_required(login_url="/amazon-login/")
def download_file(request):
    email = request.user.username
    store_name = get_storename(email)
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
    email = request.user.username
    store_name = get_storename(email)
    auth.logout(request)
    return HttpResponseRedirect("/amazon-login/")


def amazon_login(request):
    email = request.user.username
    store_name = get_storename(email)
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
    email = request.user.username
    store_name = get_storename(email)
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



def inventory_reports(request):
    email = request.user.username
    store_name = get_storename(email)
    return render(request, "inventory_reports.html", locals())




def pdf_file_view(request):
    username = request.user.username
    month = request.GET.get("month", "")
    year = request.GET.get("year", "")
    begin_date_str, end_date_str = request.GET.get("begin_date", ""), request.GET.get("end_date", "")

    # print username, month, year, begin_date_str,"||", end_date_str

    if not begin_date_str or not end_date_str:
        return render(request, "pdf_hml/2016Jun_MonthlySummary.back.html", locals())
    # print username, month, year, begin_date, end_date
    begin_date = datetime.datetime.strptime(begin_date_str.strip(), "%b %d, %Y")
    end_date = datetime.datetime.strptime(end_date_str.strip(), "%b %d, %Y")
    parmas = {"month": month, "year": year, "begin_date": begin_date, "end_date": end_date}
    spd = SummaryPdfData(username=username, **parmas)
    storename = spd.get_storename()
    product_sales = spd.product_sales()
    product_refund = spd.product_refund()
    FBA_product_sales = spd.FBA_product_sales()
    FBA_product_refund = spd.FBA_product_refund()
    FBA_invenbry_credit = spd.FB_inventory_credit()
    shipping_credits = spd.shipping_credits()
    shipping_credits_refund = spd.shipping_credits_refund()
    gift_wrap_credits = spd.gift_wrap_credits()
    gift_wrap_credits_refund = spd.gift_wrap_credits_refund()
    promotional_rebates = spd.promotional_rebates()
    promotional_rebates_refund = spd.promotional_rebates_refund()
    a_to_z_guarantee_chaims = spd.A_to_z_guarantee_claims()
    chargebacks = spd.chargebacks()
    income_subtotal_debits = spd.income_subtotal_debits([product_refund, FBA_product_refund,
                                                         shipping_credits_refund, gift_wrap_credits_refund,
                                                         promotional_rebates, a_to_z_guarantee_chaims,
                                                         chargebacks])
    income_subtotal_credits = spd.income_subtotal_credits([product_sales, FBA_product_sales,
                                                           FBA_invenbry_credit, shipping_credits,
                                                           gift_wrap_credits, promotional_rebates_refund])
    seller_fulfilled_selling_fees = spd.seller_fulfilled_selling_fees()
    FBA_selling_fees = spd.FBA_selling_fees()
    selling_fee_refund = spd.selling_fee_refund()
    fba_transaction_fees = spd.fba_transaction_fees()
    fba_transaction_fee_refunds = spd.fba_transaction_fee_refunds()
    other_transaction_fees = spd.other_transaction_fees()
    other_transaction_fee_refunds = spd.other_transaction_fee_refunds()
    FBA_inventory_inbound_services_fees = spd.FBA_inventory_inbound_services_fees()

    Shipping_label_purchases = spd.Shipping_label_purchases()
    Shipping_label_refunds = spd.Shipping_label_refunds()
    carrier_shipping_label_adjustments = spd.carrier_shipping_label_adjustments()

    Service_fees = spd.Service_fees()
    Adjustments = spd.Adjustments()
    Refund_administration_fees = spd.Refund_administration_fees()
    cost_of_advertising = spd.cost_of_advertising()
    refund_for_advertiser = spd.refund_for_advertiser()

    expense_subtotal_debits = spd.expenses_subtotal_debits([seller_fulfilled_selling_fees, FBA_selling_fees,
                                                            fba_transaction_fees, other_transaction_fees,
                                                            FBA_inventory_inbound_services_fees,
                                                            Shipping_label_purchases,
                                                            Service_fees, Refund_administration_fees,
                                                            cost_of_advertising])
    expense_subtotal_credits = spd.expenses_subtotal_credits([selling_fee_refund, fba_transaction_fee_refunds,
                                                              other_transaction_fee_refunds, Shipping_label_refunds,
                                                              carrier_shipping_label_adjustments, Adjustments,
                                                              refund_for_advertiser])
    Income = spd.Income([income_subtotal_debits, income_subtotal_credits])
    Exception = spd.Expenses([expense_subtotal_credits, expense_subtotal_debits])
    # print Income, Exception
    # print storename, product_sales, income_subtotal_debits, selling_fee_refund
    return render(request, "pdf_hml/2016Jun_MonthlySummary.html", locals())

