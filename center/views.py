# encoding:utf-8
import  json
import  datetime
from django.utils import timezone
import pytz

from django.http import StreamingHttpResponse
# from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from center.dataService.statement_view_data import StatementViewData
from django.views.decorators.csrf import csrf_exempt

from django.contrib import  auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from center.dataService.data_format import file_iterator, file_iterator_all_statement
from center.dataService.get_storename import get_storename,get_serial_number,get_store
from center.dataService.summary_pdf_data import SummaryPdfData
from center.dataService.transaction_view import TrasactionView
from  center.dataService.all_statements import AllStatementsList
from center.dataService.inventory_data import manage_fba_shipments, manage_fba_manifests

from center.dataService.inventory_report import InventoryReport, ReportType
from center.dataService.data_range_report_data import  generate_data_range_reports, generate_reports_again
from center.dataService.statement_view import StatementView

# Create your views here.


@csrf_exempt
@login_required(login_url="/amazon-login/")
def home(request):
    email = request.user.username
    store_name = get_storename(email)
    return render(request, "Home.html", locals())

@csrf_exempt
@login_required(login_url="/amazon-login/")
def inventory_reports(request):
    """INVENTORY -> Inventory Reports  """
    email = request.user.username
    store_name = get_storename(email)
    if request.GET.get("download-report") and request.GET.get("filename","") != "":
        the_file_name = request.GET.get("filename", "").replace(" ", "+")
        print "the_file_name: ", the_file_name
        fname = the_file_name.split("/")[-1]
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"'%str(fname)
        return response
    else:
        report_type = request.GET.get("report_type", "")
        report_type_text = ReportType().get_report_type(report_type)
        print report_type_text
        datas_list = InventoryReport(username=email).get_report_recorde()
        return render(request, "inventory_reports.html", locals())

@login_required(login_url="/amazon-login/")
def listing_reports(request):
    """分页列出 data range reports 里面的generate reports 列"""
    email = request.user.username
    store_name = get_storename(email)
    report_count = request.GET.get("report_count", "10")
    page = request.GET.get("page", 1)
    datas_list = InventoryReport(username=email).get_report_recorde(count=report_count,page=page)
    return render(request, "inventory_reports.html", locals())
    

@csrf_exempt
@login_required(login_url="/amazon-login/")
def inventory_reports_data(request):
    email = request.user.username
    store_name = get_storename(email)
    report_type = request.GET.get("report_type", "")
    report_type_text = ReportType().get_report_type(report_type)
    print  report_type_text
    if request.method == "POST":
        print "inventory_reports_data:", request.POST
        report_type = request.POST.get("reportVariant", "")
        print report_type
        InventoryReport(username=email).get_inventory_report(report_type)
        #return HttpResponseRedirect("/inventory/inventory-reports/?from=inventory-reports-data&report_type="+report_type)
    datas_list = InventoryReport(username=email).get_report_recorde()
    return HttpResponseRedirect("/inventory/inventory-reports/?from=inventory-reports-data&report_type="+report_type)


@login_required(login_url="/amazon-login/")
def inventory_FBA_shipping(request):
    email = request.user.username
    store_name = get_storename(email)
    return render(request, "inventory_FBA_shipping.html", locals())

@csrf_exempt
@login_required(login_url="/amazon-login/")
def inventory_FBA_shipping_shipments(request):
    # if request.method == "POST":
    datas = manage_fba_shipments()
    return HttpResponse(datas)


@csrf_exempt
@login_required(login_url="/amazon-login/")
def inventory_FBA_shipping_manifests(request):
    datas = manage_fba_manifests()
    return HttpResponse(datas)



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
    date_time_list = ["Oct 15, 2016 - Nov 23, 2016", "Oct 1, 2016 - Oct 15, 2016",
                      "Mar 19, 2016 - Oct 1, 2016", "Feb 6, 2016 - Mar 19, 2016"]
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
    groupId = request.GET.get("groupId", "")
    print groupId
    view = request.GET.get("view", "")
    recorde_result = TrasactionView(username,request.GET).get_transaction_view()
    # print recorde_result
    recorde_list = recorde_result.get("recorde_list", [])
    start_item = recorde_result.get("start_item", 1)
    end_item = recorde_result.get("end_item", 1)
    total_page = recorde_result.get("total_page", 1)
    next_page = int(recorde_result.get("next_page", 1))
    date_time_list = ["Oct 15, 2016 - Nov 23, 2016", "Oct 1, 2016 - Oct 15, 2016",
                      "Mar 19, 2016 - Oct 1, 2016","Feb 6, 2016 - Mar 19, 2016"]
    if total_page <= 10:
        total_page_list = xrange(1, total_page + 1)
    else:
        total_page_list = xrange(1, total_page + 1)
    pre_page = 0 if cur_page  <= 0 else int(cur_page) - 1
    return render(request, "transaction.html", locals())


#ict: {u'pageSize': [u'Ten'], u'eventType': [u'Refund'], u'mostRecentLast': [u'0'], u'Update': [u''], u'subview': [u'groups'], u'searchLanguage': [u'en_US'], u'groupId': [u'2016290Df-4nXYET2mOMsbCKQkt8Q'], u'view': [u'filter']}>


@login_required(login_url="/amazon-login/")
def transaction_data_download(request):
    username = request.user.username
    the_file_name = TrasactionView(username,request.GET).write_report_to_txt()
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("report.txt")
    return response








@login_required(login_url="/amazon-login/")
def all_statements(request):
    email = request.user.username
    store_name = get_storename(email)
    all_statements_list = AllStatementsList(email).get_all_statements_file()
    today =  datetime.datetime.now().strftime('%m/%d/%Y');
    startDate = endDate = today
    # print all_statements_list
    return render(request, 'all_statements.html', locals())

@login_required(login_url="/amazon-login/")
def download_all_statements(request):
    email = request.user.username
    print request.GET
    file_type = request.GET.get("file_type", "octet-stream")    #vnd.ms-excel (.xls),  octet-stream(pdf) 下载文件
    file_name = request.GET.get("file_name", "not_found_file_name")
    print "file_type:", file_type, "file_name: ", file_name
    if not file_name:
        return HttpResponseRedirect("/all-statements/")
    try:
        response = StreamingHttpResponse(file_iterator_all_statement(file_name))
    except Exception, e:
        print "file str Error, %s" % str(e)
        return HttpResponseRedirect("/all-statements/")
    response['Content-Type'] = 'application/' + str(file_type)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


@login_required(login_url="/amazon-login/")
@csrf_exempt
def request_report_again(request):
    """再次生成report_pdf """
    line_id = request.GET.get("line_id", "")
    username = request.user.username
    generate_reports_again(line_id, username)
    return HttpResponseRedirect("/date-range-reports/")


@login_required(login_url="/amazon-login/")
@csrf_exempt
def date_range_reports(request):
    """导出pdf的 """
    email = request.user.username
    store_name = get_storename(email)
    if request.method == "POST":
        print "="* 100
        print "request post: ",request.POST
        result = generate_data_range_reports(request)
        #result = {"statusCode":"OK"}  #用这个字典，前端才会正常
        return HttpResponse(json.dumps(result))
    else:
        pageSize = request.GET.get("pageSize",10)
        cur_page = int(request.GET.get("cur_page",1))
        pageSize = 10 if pageSize == 10 or pageSize == "10" or pageSize == "Ten" else 10
        username,post_dict,return_dict = request.user.username, request.POST, {}
        recorde_result = StatementViewData(username, post_dict, return_dict).statement_data_read(**{"pageSize":pageSize,"cur_page":cur_page})
        recorde_list = recorde_result.get("recorde_list", [])
        start_item = recorde_result.get("start_item",1)
        end_item   = recorde_result.get("end_item",1)
        total_page = recorde_result.get("total_page", 1)
        next_page = recorde_result.get("next_page", 1)
        next_page = int(recorde_result.get("next_page", 1))
        total_page_list = range(1, total_page + 1)
        pre_page = 0 if cur_page <= 0 else int(cur_page) - 1
        total_count = recorde_result.get("total_count",0)
        # print recorde_list
        return  render(request, "data_range_reports.html", locals())


    
@login_required(login_url="/amazon-login/")
def statement_view(request):
    email = request.user.username
    serial_number = get_serial_number(email)
    store = get_store(email)
    # store_name = get_storename(email)
    # result_dict = StatementViewData(request).test_return()
    groupid = request.GET.get("groupId", "")
    result_dict = {"unsuccessful_charges": 0}
    dateGroups = []
    tz = pytz.utc
    start_date = datetime.datetime.strptime(store.payment_time.split('+')[0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz)
    end_date = start_date + datetime.timedelta(days=14)
    now_date = timezone.now()
    print now_date
    while end_date < now_date:
        start_date_str = start_date.strftime('%b %d, %Y')
        end_date_str = end_date.strftime('%b %d, %Y')
        date_group_item = start_date_str + " - "+end_date_str
        if date_group_item == groupid:
            curent_date_group_item_end = end_date_str
            dateGroups.insert(0, {"value": date_group_item,'selected':True})
        else:
            dateGroups.insert(0, {"value": date_group_item})
        start_date = end_date
        end_date = start_date + datetime.timedelta(days=14)
    current_date_group = start_date.strftime('%b %d, %Y') + " - " + now_date.strftime('%b %d, %Y')
    if groupid:
        start_time = datetime.datetime.strptime(groupid.split('-')[0].strip(),'%b %d, %Y')
        end_time = datetime.datetime.strptime(groupid.split('-')[1].strip(),'%b %d, %Y')
    else:
        return render(request, 'statement_view.html', locals())
    stvs = StatementView.objects.filter(serial_number=serial_number,date_time__range=(start_time, end_time))

    product_charges_order = 0.0
    promo_rebates_order = 0.0
    amazon_fees_order = 0.0
    other_order = 0.0

    product_charges_refunds = 0.0
    promo_rebates_refunds = 0.0
    amazon_fees_refunds = 0.0
    other_refunds = 0.0

    fba_inventory_fee = 0.0
    cost_of_advertising = 0.0
    fba_fee = 0.0
    other = 0.0

    for stv in stvs:
        if stv.type =="Order":
            product_charges_order += float(stv.product_sales)
            promo_rebates_order += float(stv.promotional_rebates)
            amazon_fees_order += float(stv.selling_fees)+float(stv.fba_fees)+float(stv.other_transaction_fees)
            other_order += float(stv.shipping_credits)+float(stv.gift_wrap_credits)
        elif stv.type == "Refunds":
            product_charges_refunds += float(stv.product_sales)
            promo_rebates_refunds += float(stv.promotional_rebates)
            amazon_fees_refunds += float(stv.selling_fees) + float(stv.fba_fees) + float(stv.other_transaction_fees)
            other_refunds += float(stv.shipping_credits) + float(stv.gift_wrap_credits)
        elif stv.type == "FBA Inventory Fee":
            fba_inventory_fee += float(stv.total)
        elif stv.type == "Service Fee":
            if stv.description == "Cost of Advertising":
                cost_of_advertising += float(stv.total)
            else:
                fba_fee += float(stv.total)
        else:
            other += float(stv.total)

    order = {'product_charges':{'value':product_charges_order,'flag':product_charges_order>=0},
             'promo_rebates':{'value':promo_rebates_order,'flag':promo_rebates_order>=0},
             'amazon_fees':{'value':amazon_fees_order,'flag':amazon_fees_order>=0},
             'other':{'value':other_order,'flag':other_order>=0},
             'sub_total':product_charges_order+promo_rebates_order+amazon_fees_order+other_order}
    refunds = {'product_charges':{'value':product_charges_refunds,'flag':product_charges_refunds>=0},
               'promo_rebates':{'value':promo_rebates_refunds,'flag':promo_rebates_refunds>=0},
               'amazon_fees':{'value':amazon_fees_refunds,'flag':amazon_fees_refunds>=0},
               'other':{'value':other_refunds,'flag':other_refunds>=0},
               'sub_total':product_charges_refunds+promo_rebates_refunds+amazon_fees_refunds+other_refunds}
    selling_fee = {'fba_fee':{'value':fba_fee,'flag':fba_fee>=0},
                   'cost_of_advertising':{'value':cost_of_advertising,'flag':cost_of_advertising>=0},
                   'fba_inventory_fee':{'value':fba_inventory_fee,'flag':fba_inventory_fee>=0},
                   'sub_total':fba_fee+cost_of_advertising+fba_inventory_fee}
    other = {'other':other,'flag':other>=0}
    result_dict.update({"seller_repayment":order.get('sub_total')+refunds.get('sub_total')+selling_fee.get('sub_total')+other.get('other')})
    result_dict.update({"all_seller_repayment":result_dict.get('seller_repayment')+result_dict.get('unsuccessful_charges')})
    result_dict.update({"change_date":end_date.strftime('%b %d, %Y')})

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

@csrf_exempt
def amazon_login(request):
    email = request.user.username
    store_name = get_storename(email)
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        print email, password
        user = auth.authenticate(username=email, password=password)
        if user and email != "root@starmerx.com":
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













def pdf_file_view(request):
    """ 这里是显示页面, 真正生成pdf的html在summary_pdf_data.py里面的create_pdf_from_html"""
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
    legal_name = spd.get_legal_name()
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

