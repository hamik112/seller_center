#!/usr/bin/env python
# encoding:utf-8

import  datetime

import  os
from django.conf import settings
from django.db.models import Q
from django.db.models import  Sum
from django.template import  Template, Context

from center.dataService.phantojs_to_pdf import html_to_pdf
from manageApp.models import FilenameToStorename
from manageApp.models import StatementView,StatementViewMonth
from SellerCenter.utils import str_to_float

def oredits_number_len(number_str):
    # y = -0.278x + 31.97  --> x 为 product_sale_sum 的长度， 即: len(product_sale_sum)
    x = len(str(number_str))
    return -0.278 * x + 31.97

def debits_number_len(number_str):
    # y = -0.2757 * x + 26.1824  --> x 为 product_sale_sum 的长度， 即: len(product_sale_sum)
    x = len(str(number_str))
    return -0.2757 * x + 26.1824

## 右边 ##
def expense_debits_len(number_str):
    x = len(str(number_str))
    return -0.264275 * x + 58.153475

def expend_credicts_len(number_str):
    x = len(str(number_str))
    # return -0.297 * x + 65.227875
    return -0.29216499999999995 * x + 63.958864999999996


def Income_len(number_str):
    x = len(str(number_str))
    return -0.475 * x + 31.943

def Expenses_len(number_str):
    x = len(str(number_str))
    return -0.452745 * x  + 63.742705



def number_format(num):
    if float(num) > 0 or float(num) < 0:
        num = str("%.2f"%float(num))
    else:
        num = 0
    if float(num) >= 1000 or float(num) <= -1000:
        num = format(float(num),",")
    return str(num)






class SummaryPdfData(object):
    def __init__(self, username, **params):
        self.username = username
        self.year = params.get("year", "")
        self.month = params.get("month", "")
        self.begin_date = params.get("begin_date", "")
        self.end_date = params.get("end_date", "")
        self.serial_number = self.get_serial_number()

    def get_serial_number(self):
        try:
            serial_number = FilenameToStorename.objects.filter(email=self.username).values_list("serial_number", flat=True)[0]
        except Exception, e:
            serial_number = ""
        return serial_number

    def get_storename(self):
        try:
            storename = FilenameToStorename.objects.filter(serial_number=self.serial_number).values_list("storename", flat=True)[0]
        except Exception, e:
            print str(e)
            storename = ""
        return storename

    def get_legal_name(self):
        try:
            legal_name = FilenameToStorename.objects.filter(serial_number=self.serial_number).values_list("manager",flat=True)[0]
        except Exception, e:
            legal_name = ""
        print "legal_name:", legal_name
        return legal_name


    def product_sales(self):
        # print self.serial_number
        query_select = Q(serial_number=self.serial_number, type="Order", fulfillment="Seller")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            product_sale_query_dict = StatementView.objects.filter(query_select).values("product_sales", "other").aggregate(Sum("product_sales"),Sum("other"))
        except Exception, e:
            product_sale_query_dict = {}
        print "product_sale: ", product_sale_query_dict
        if product_sale_query_dict.get("product_sales__sum") != None and product_sale_query_dict.get("other__sum") != None:
            product_sale_sum = product_sale_query_dict.get("product_sales__sum", 0) + product_sale_query_dict.get("other__sum", 0)
        else:
            product_sale_sum = 0
        product_sale_sum = number_format(product_sale_sum)
        product_sale_html_sum = oredits_number_len(product_sale_sum)
        print "product_sale_sum", product_sale_sum
        return {"number_length": product_sale_html_sum, "number": product_sale_sum}


    def product_refund(self):
        query_select = Q(serial_number=self.serial_number, type="Refund", fulfillment="Seller")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            product_refund_query_dict = StatementView.objects.filter(query_select).values("product_sales", "other").aggregate(Sum("product_sales"),Sum("other"))
        except Exception, e:
            product_refund_query_dict = {}
        if product_refund_query_dict.get("product_sales__sum") != None and product_refund_query_dict.get("other__sum") != None:
            product_refund_sum = product_refund_query_dict.get("product_sales__sum") + product_refund_query_dict.get("other__sum")
        else:
            product_refund_sum = 0
        product_refund_sum = number_format(product_refund_sum)
        return {"number_length": debits_number_len(product_refund_sum), "number": product_refund_sum}


    def FBA_product_sales(self):
        # print self.serial_number
        query_select = Q(serial_number=self.serial_number, type="Order", fulfillment="Amazon")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            product_sale_query_dict = StatementView.objects.filter(query_select).values("product_sales", "other").aggregate(Sum("product_sales"),Sum("other"))
        except Exception, e:
            product_sale_query_dict = {}
        if product_sale_query_dict.get("product_sales__sum") !=None and product_sale_query_dict.get("other__sum") != None:
            product_sale_sum = product_sale_query_dict.get("product_sales__sum", 0) + product_sale_query_dict.get("other__sum", 0)
        else:
            product_sale_sum = 0
        product_sale_sum = number_format(product_sale_sum)
        product_sale_html_sum = oredits_number_len(product_sale_sum)
        return {"number_length": product_sale_html_sum, "number": product_sale_sum}


    def FBA_product_refund(self):
        query_select = Q(serial_number=self.serial_number, type="Refund", fulfillment="Amazon")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            product_refund_query_dict = StatementView.objects.filter(query_select).values("product_sales", "other").aggregate(Sum("product_sales"),Sum("other"))
        except Exception, e:
            product_refund_query_dict = {}
        if product_refund_query_dict.get("product_sales__sum") != None and product_refund_query_dict.get("other__sum") != None:
            product_refund_sum = product_refund_query_dict.get("product_sales__sum") + product_refund_query_dict.get("other__sum")
        else:
            product_refund_sum = 0
        # product_refund_sum = format(product_refund_sum, ",")
        product_refund_sum = number_format(product_refund_sum)
        return {"number_length": debits_number_len(product_refund_sum), "number": product_refund_sum}


    def FB_inventory_credit(self):
        """ FBA inventory credit	C(type)的adjustment 对应的total减去 expense中的Adjustments"""
        query_select = Q(serial_number=self.serial_number, type="Adjustment")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            inventory_credit_dict = StatementView.objects.filter(query_select).values("total").aggregate(Sum("total"))
        except Exception, e:
            inventory_credit_dict = {}
        if inventory_credit_dict.get("total__sum") != None:
            products_credit_sum = inventory_credit_dict.get("total__sum", 0)
        else:
            products_credit_sum = 0
        products_credit_sum = products_credit_sum - 0 # expense中的Adjustments"一般为0
        # products_credit_sum = format(products_credit_sum, ",")
        products_credit_sum = number_format(products_credit_sum)
        return {"number_length": oredits_number_len(products_credit_sum), "number": products_credit_sum}



    def shipping_credits(self):
        """ Order 对应的N """
        query_select = Q(serial_number=self.serial_number, type="Order")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            shipping_credits_dict = StatementView.objects.filter(query_select).values("shipping_credits").aggregate(Sum("shipping_credits"))
        except Exception, e:
            shipping_credits_dict = {}
        print shipping_credits_dict
        if shipping_credits_dict.get("shipping_credits__sum", "") != None:
            shipping_credits_sum = shipping_credits_dict.get("shipping_credits__sum", 0)
        else:
            shipping_credits_sum = 0
        # shipping_credits_sum = format(shipping_credits_sum, ",")
        shipping_credits_sum = number_format(shipping_credits_sum)
        return {"number_length": oredits_number_len(shipping_credits_sum), "number": shipping_credits_sum}

    def shipping_credits_refund(self):
        """ Refund 对应的N """
        query_select = Q(serial_number=self.serial_number, type="Refund")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            shipping_credits_refund_dict = StatementView.objects.filter(query_select).values("shipping_credits").aggregate(Sum("shipping_credits"))
        except Exception, e:
            shipping_credits_refund_dict = {}
        if shipping_credits_refund_dict.get("shipping_credits__sum", "") != None:
            shipping_credits_refund_sum = shipping_credits_refund_dict.get("shipping_credits__sum", 0)
        else:
            shipping_credits_refund_sum = 0
        # shipping_credits_refund_sum = format(shipping_credits_refund_sum, ",")
        shipping_credits_refund_sum = number_format(shipping_credits_refund_sum)
        return {"number_length": debits_number_len(shipping_credits_refund_sum), "number": shipping_credits_refund_sum}

    def gift_wrap_credits(self):
        """ Order 对应的O 列"""
        query_select = Q(serial_number = self.serial_number, type="Order")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            gift_wrap_credits_dict = StatementView.objects.filter(query_select).values("gift_wrap_credits").aggregate(Sum("gift_wrap_credits"))
        except Exception, e:
            gift_wrap_credits_dict = {}
        if gift_wrap_credits_dict.get("gift_wrap_credits__sum") != None:
            gift_wrap_credits_sum = gift_wrap_credits_dict.get("gift_wrap_credits__sum", 0)
        else:
            gift_wrap_credits_sum = 0
        # gift_wrap_credits_sum = format(gift_wrap_credits_sum, ",")
        gift_wrap_credits_sum = number_format(gift_wrap_credits_sum)
        return {"number_length": oredits_number_len(gift_wrap_credits_sum), "number": gift_wrap_credits_sum}

    def gift_wrap_credits_refund(self):
        """ Refund 对应的O 列"""
        query_select = Q(serial_number = self.serial_number, type="Refund")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            gift_wrap_credits_refund_dict = StatementView.objects.filter(query_select).values("gift_wrap_credits").aggregate(Sum("gift_wrap_credits"))
        except Exception, e:
            gift_wrap_credits_refund_dict = {}
        print gift_wrap_credits_refund_dict
        if gift_wrap_credits_refund_dict.get("gift_wrap_credits__sum") != None:
            gift_wrap_credits_refund_sum = gift_wrap_credits_refund_dict.get("gift_wrap_credits__sum", 0)
        else:
            gift_wrap_credits_refund_sum = 0
        # gift_wrap_credits_sum = format(gift_wrap_credits_refund_sum, ",")
        gift_wrap_credits_sum = number_format(gift_wrap_credits_refund_sum)
        return {"number_length": debits_number_len(gift_wrap_credits_sum), "number": gift_wrap_credits_sum}

    def promotional_rebates(self):
        """Order对应的P列 """
        query_select = Q(serial_number = self.serial_number, type="Order")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            promotional_rebates_dict = StatementView.objects.filter(query_select).values("promotional_rebates").aggregate(Sum("promotional_rebates"))
        except Exception, e:
            promotional_rebates_dict = {}
        print promotional_rebates_dict
        if promotional_rebates_dict.get("promotional_rebates__sum") != None:
            promotional_rebates_sum = promotional_rebates_dict.get("promotional_rebates__sum", 0)
        else:
            promotional_rebates_sum = 0
        promotional_rebates_sum = format(promotional_rebates_sum, ",")
        return {"number_length": debits_number_len(promotional_rebates_sum), "number": promotional_rebates_sum}

    def promotional_rebates_refund(self):
        """Refund对应的P列 """
        query_select = Q(serial_number = self.serial_number, type="Refund")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            promotional_rebates_refund_dict = StatementView.objects.filter(query_select).values("promotional_rebates").aggregate(Sum("promotional_rebates"))
        except Exception, e:
            promotional_rebates_refund_dict = {}
        if promotional_rebates_refund_dict.get("promotional_rebates__sum") != None:
            promotional_rebates_sum = promotional_rebates_refund_dict.get("promotional_rebates__sum", 0)
        else:
            promotional_rebates_sum = 0
        promotional_rebates_sum = number_format(promotional_rebates_sum)
        return {"number_length": oredits_number_len(promotional_rebates_sum), "number": promotional_rebates_sum}

    def A_to_z_guarantee_claims(self):
        """ atz 对应的 total   """
        query_select = Q(serial_number = self.serial_number, type="A-to-z Guarantee Glaim")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            a_to_z_gurantee_claim_dict = StatementView.objects.filter(query_select).values("total").aggregate(Sum("total"))
        except Exception, e:
            a_to_z_gurantee_claim_dict = {}
        if a_to_z_gurantee_claim_dict.get("total__sum") != None:
            a_to_z_gurantee_claim_sum = a_to_z_gurantee_claim_dict.get("total__sum", 0)
        else:
            a_to_z_gurantee_claim_sum = 0
        a_to_z_gurantee_claim_sum = number_format(a_to_z_gurantee_claim_sum)
        return {"number_length": debits_number_len(a_to_z_gurantee_claim_sum), "number":a_to_z_gurantee_claim_sum}


    def chargebacks(self):
        """ chargebacks 对应的 total """
        query_select = Q(serial_number = self.serial_number, type="Chargebacks")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            chargebacks_dict = StatementView.objects.filter(query_select).values("total").aggregate(Sum("total"))
        except Exception, e:
            chargebacks_dict = {}
        if chargebacks_dict.get("total__sum") != None:
            chargebacks_sum = chargebacks_dict.get("total__sum", 0)
        else:
            chargebacks_sum = 0
        chargebacks_sum = number_format(chargebacks_sum)
        return {"number_length": debits_number_len(chargebacks_sum), "number": chargebacks_sum}


    def income_subtotal_debits(self, subtotal_list):
        income_subtotal_debits_number = sum([float(i.get("number", '0').replace(",", "")) for i in subtotal_list])
        income_subtotal_debits_number = number_format(income_subtotal_debits_number)
        return {"number_length": debits_number_len(income_subtotal_debits_number), "number": income_subtotal_debits_number}

    def income_subtotal_credits(self, subtotal_list):
        income_subtotal_debits_number = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        income_subtotal_debits_number = number_format(income_subtotal_debits_number)
        return  {"number_length": oredits_number_len(income_subtotal_debits_number), "number": income_subtotal_debits_number}


    #----------------------  Expenses   --------------------------
    def seller_fulfilled_selling_fees(self):
        """ type(Order) + R列数据"""
        query_select = Q(serial_number = self.serial_number, type="Order", fulfillment="Seller")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            seller_fulfilled_selling_fees_dict = StatementView.objects.filter(query_select).values("selling_fees").aggregate(Sum("selling_fees"))
        except Exception, e:
            seller_fulfilled_selling_fees_dict = {}
        if seller_fulfilled_selling_fees_dict.get("selling_fees__sum") != None:
            seller_fulfilled_selling_fees_sum = seller_fulfilled_selling_fees_dict.get("selling_fees__sum", 0)
        else:
            seller_fulfilled_selling_fees_sum = 0
        seller_fulfilled_selling_fees_sum = number_format(seller_fulfilled_selling_fees_sum)
        print "seller_fulfilled_selling_fees_sum: ", seller_fulfilled_selling_fees_sum
        return {"number_length":expense_debits_len(seller_fulfilled_selling_fees_sum), "number":seller_fulfilled_selling_fees_sum}


    def FBA_selling_fees(self):
        """ type(Order)+I(Amazon)的R列的和"""
        query_select = Q(serial_number = self.serial_number, type="Order", fulfillment="Amazon")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))

        try:
            FBA_selling_fees_dict = StatementView.objects.filter(query_select).values("selling_fees").aggregate(Sum("selling_fees"))
        except Exception, e:
            FBA_selling_fees_dict = {}
        if FBA_selling_fees_dict.get("selling_fees__sum") != None:
            FBA_selling_fees_sum = FBA_selling_fees_dict.get("selling_fees__sum", 0)
        else:
            FBA_selling_fees_sum = 0
        FBA_selling_fees_sum = number_format(FBA_selling_fees_sum)
        return {"number_length": expense_debits_len(FBA_selling_fees_sum), "number": FBA_selling_fees_sum}


    def selling_fee_refund(self):
        """ type(Refund) 对应的R列减去下面B的项值 """
        query_select = Q(serial_number = self.serial_number, type="Refund")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            selling_fee_refund_dict = StatementView.objects.filter(query_select).values("selling_fees").aggregate(Sum("selling_fees"))
        except Exception, e:
            selling_fee_refund_dict = {}
        print "selling_fee_refund: ", selling_fee_refund_dict
        if selling_fee_refund_dict.get("selling_fees__sum") != None:
            selling_fee_refund_sum = selling_fee_refund_dict.get("selling_fees__sum", 0)
        else:
            selling_fee_refund_sum = 0
        selling_fee_refund_sum = number_format(selling_fee_refund_sum)
        return {"number_length": expend_credicts_len(selling_fee_refund_sum), "number":selling_fee_refund_sum}


    def fba_transaction_fees(self):
        """ tyoe(Order)对应的S列 """
        query_select = Q(serial_number = self.serial_number, type="Order", fulfillment="Amazon")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            fba_trasaction_fees_dict = StatementView.objects.filter(query_select).values("fba_fees").aggregate(Sum("fba_fees"))
        except Exception, e:
            fba_trasaction_fees_dict = {}
        if fba_trasaction_fees_dict.get("fba_fees__sum") != None:
            fba_trasaction_fees_sum = fba_trasaction_fees_dict.get("fba_fees__sum", 0)
        else:
            fba_trasaction_fees_sum = 0
        fba_trasaction_fees_sum = number_format(fba_trasaction_fees_sum)
        return {"number_length": expense_debits_len(fba_trasaction_fees_sum), "number": fba_trasaction_fees_sum}


    def fba_transaction_fee_refunds(self):
        """ type(Refund)对应的S """
        query_select = Q(serial_number = self.serial_number, type="Refund")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            fba_transaction_fee_refund_dict = StatementView.objects.filter(query_select).values("fba_fees").aggregate(Sum("fba_fees"))
        except Exception, e:
            fba_transaction_fee_refund_dict = {}
        if fba_transaction_fee_refund_dict.get("fba_fees__sum"):
            fba_transaction_fee_refund_sum = fba_transaction_fee_refund_dict.get("fba_fees__sum", 0)
        else:
            fba_transaction_fee_refund_sum = 0
        fba_transaction_fee_refund_sum = number_format(fba_transaction_fee_refund_sum)
        return {"number_length": expend_credicts_len(fba_transaction_fee_refund_sum), "number": fba_transaction_fee_refund_sum}


    def other_transaction_fees(self):
        """ type(Order) 的T列的数和"""
        query_select = Q(serial_number = self.serial_number, type="Order")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            other_transaction_fee_dict = StatementView.objects.filter(query_select).values("other_transaction_fees").aggregate(Sum("other_transaction_fees"))
        except Exception, e:
            other_transaction_fee_dict = {}
        if other_transaction_fee_dict.get("other_transaction_fees__sum"):
            other_transaction_fee_sum = other_transaction_fee_dict.get("other_transaction_fees__sum", 0)
        else:
            other_transaction_fee_sum = 0
        other_transaction_fee_sum = number_format(other_transaction_fee_sum)
        return {"number_length": expense_debits_len(other_transaction_fee_sum), "number": other_transaction_fee_sum}


    def other_transaction_fee_refunds(self):
        """ type(Refund) 对应T列的值 之和 """
        query_select = Q(serial_number=self.serial_number, type="Refund")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            other_transaction_fee_refund_dict = StatementView.objects.filter(query_select).values("other_transaction_fees").aggregate(Sum("other_transaction_fees"))
        except Exception, e:
            other_transaction_fee_refund_dict = {}
        if other_transaction_fee_refund_dict.get("other_transaction_fees__sum"):
            other_transaction_fee_refund_sum = other_transaction_fee_refund_dict.get("other_transaction_fees__sum", 0)
        else:
            other_transaction_fee_refund_sum = 0
        other_transaction_fee_refund_sum = number_format(other_transaction_fee_refund_sum)
        return {"number_length": expend_credicts_len(other_transaction_fee_refund_sum), "number": other_transaction_fee_refund_sum}


    def FBA_inventory_inbound_services_fees(self):
        """ type(FBA inventory fee & FB Customer Return Fee)的total之和"""
        query_select  = Q(serial_number = self.serial_number, type__in=["FBA Inventory Fee", "FBA Customer Return Fee"])
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            FBA_inventory_inbound_services_dict = StatementView.objects.filter(query_select).values("total").aggregate(Sum("total"))
        except Exception, e:
            FBA_inventory_inbound_services_dict = {}
        print "FBA_inventory_inbound_services_dict: ", FBA_inventory_inbound_services_dict
        if FBA_inventory_inbound_services_dict.get("total__sum"):
            FBA_inventory_inbound_services_sum = FBA_inventory_inbound_services_dict.get("total__sum", 0)
        else:
            FBA_inventory_inbound_services_sum = 0
        print "FBA_inventory_inbound_services_sum: ", FBA_inventory_inbound_services_sum
        FBA_inventory_inbound_services_sum =  number_format(FBA_inventory_inbound_services_sum)
        return {"number_length": expense_debits_len(FBA_inventory_inbound_services_sum), "number": FBA_inventory_inbound_services_sum}

    def Shipping_label_purchases(self):
        """ """
        shipping_label_purchases = '0'
        return {"number_length": expense_debits_len(shipping_label_purchases), "number": shipping_label_purchases}

    def Shipping_label_refunds(self):
        shipping_label_refunds = '0'
        return {"number_length": expend_credicts_len(shipping_label_refunds), "number": shipping_label_refunds}

    def carrier_shipping_label_adjustments(self):
        """ """
        carrier_shipping_label_adjustment_sum = '0'
        return {"number_length": expend_credicts_len(carrier_shipping_label_adjustment_sum), "number": carrier_shipping_label_adjustment_sum}

    def Service_fees(self):
        """ type(Service fees) 的total 之和 """
        query_select = Q(serial_number=self.serial_number, type="Service Fee", description="Subscription Fee")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            service_fees_dict = StatementView.objects.filter(query_select).values("total").aggregate(Sum("total"))
        except Exception, e:
            service_fees_dict = {}
        if service_fees_dict.get("total__sum"):
            service_fees_sum = service_fees_dict.get("total__sum", 0)
        else:
            service_fees_sum = 0
        service_fees_sum = number_format(service_fees_sum)
        return {"number_length": expense_debits_len(service_fees_sum), "number": service_fees_sum}


    def Refund_administration_fees(self):
        """ 这项不变 """
        refund_administration_fees_sum = 0
        return {"number_length":expense_debits_len(refund_administration_fees_sum), "number":refund_administration_fees_sum}

    def Adjustments(self):
        adjuestments_sum = 0
        return {"number_length": expend_credicts_len(adjuestments_sum), "number": adjuestments_sum}

    def cost_of_advertising(self):
        cost_of_advertising_sum = 0
        query_select = Q(serial_number=self.serial_number, type="Service Fee", description="Cost of Advertising")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            service_fees_dict = StatementView.objects.filter(query_select).values("total").aggregate(Sum("total"))
        except Exception, e:
            service_fees_dict = {}
        if service_fees_dict.get("total__sum"):
            cost_of_advertising_sum = service_fees_dict.get("total__sum", 0)
        else:
            cost_of_advertising_sum = 0
            cost_of_advertising_sum = number_format(cost_of_advertising_sum)
        return {"number_length": expense_debits_len(cost_of_advertising_sum), "number": cost_of_advertising_sum}


    def refund_for_advertiser(self):
        refund_for_advertiser_sum = 0
        return {"number_length": expend_credicts_len(refund_for_advertiser_sum), "number": refund_for_advertiser_sum}

    def expenses_subtotal_debits(self, subtotal_list):
        """ expenses debits  total """
        income_subtotal_debits_number = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        income_subtotal_debits_number = number_format(income_subtotal_debits_number)
        return {"number_length": expense_debits_len(income_subtotal_debits_number), "number": income_subtotal_debits_number}

    def expenses_subtotal_credits(self, subtotal_list):
        """ expenses credits  total """
        income_subtotal_debits_number = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        income_subtotal_debits_number = number_format(income_subtotal_debits_number)
        return {"number_length": expend_credicts_len(income_subtotal_debits_number), "number": income_subtotal_debits_number}


    def Income(self, subtotal_list):
        Income_sum = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        Income_sum = number_format(Income_sum)
        return {"number_length":Income_len(Income_sum), "number": Income_sum}

    def summaries_income(self,subtotal_list):
        Income_sum = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        Income_sum = number_format(Income_sum)
        return {"number_length":expend_credicts_len(Income_sum), "number": Income_sum}

    def Expenses(self, subtotal_list):
        expenses_number = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        expenses_number = number_format(expenses_number)
        return {"number_length": Expenses_len(expenses_number), "number": expenses_number}

    def summaries_expenses(self, subtotal_list):
        expenses_number = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        expenses_number = number_format(expenses_number)
        return {"number_length": expend_credicts_len(expenses_number), "number": expenses_number}

    def transfers_to_bank_account(self):
        query_select = Q(serial_number= self.serial_number, type="Transfer")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            transfers_to_bank_account_dict = StatementView.objects.filter(query_select).values("total").aggregate(Sum("total"))
        except Exception,e:
            transfers_to_bank_account_dict = {}
        if transfers_to_bank_account_dict.get("total__sum") != None:
            transfers_to_bank_account_sum = transfers_to_bank_account_dict.get("total__sum", 0)
        else:
            transfers_to_bank_account_sum = 0
        transfers_to_bank_account_sum = number_format(transfers_to_bank_account_sum)
        return {"number_length": debits_number_len(transfers_to_bank_account_sum), "number":transfers_to_bank_account_sum}

    def failed_transfer_to_bank_account(self):
        failed_transfer_to_bank_account_sum = 0
        return {"number_length":debits_number_len(failed_transfer_to_bank_account_sum), "number":failed_transfer_to_bank_account_sum}


    def charges_to_credit_card(self):
        query_select = Q(serial_number=self.serial_number, type="Debt")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            charges_to_credit_dict = StatementView.objects.filter(query_select).values("total").aggregate(Sum("total"))
        except Exception, e:
            charges_to_credit_dict = {}
        print "charges_to_credit_card: ", charges_to_credit_dict
        if charges_to_credit_dict.get("total__sum"):
            product_sale_sum = charges_to_credit_dict.get("total__sum",0)
        else:
            product_sale_sum = 0
        product_sale_sum = number_format(product_sale_sum)
        product_sale_html_sum = oredits_number_len(product_sale_sum)
        return {"number_length": product_sale_html_sum, "number": product_sale_sum}

    def Transfers(self, subtotal_list):
        transfers_sum = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        transfers_sum = number_format(transfers_sum)
        print "transfers_sum:", transfers_sum
        return {"number_length":Income_len(transfers_sum), "number": transfers_sum}
    def sub_credits_transfers(self, subtotal_list):
        transfers_sum = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        transfers_sum = number_format(transfers_sum)
        return {"number_length": oredits_number_len(transfers_sum), "number": transfers_sum}

    def summaries_transfers(self,subtotal_list):
        transfers_number = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        transfers_number = number_format(transfers_number)
        return {"number_length": expend_credicts_len(transfers_number), "number": transfers_number}





def generate_dict(**param_dict):
    year = param_dict.get("year", "")
    begin_date_str, end_date_str = param_dict.get("begin_date_str",""), param_dict.get("end_date_str", "")
    username, month= param_dict.get("username",""),param_dict.get("month","")
    if  begin_date_str and  end_date_str:
        begin_date = datetime.datetime.strptime(begin_date_str.strip(), "%b %d, %Y")
        end_date = datetime.datetime.strptime(end_date_str.strip(), "%b %d, %Y") + datetime.timedelta(days=1)  #date_time__range不包含最后一天
    else:
        begin_date, end_date = datetime.datetime.now(), datetime.datetime.now()
    # print username, month, year, begin_date, end_date
    parmas = {"month":month, "year":year, "begin_date":begin_date, "end_date":end_date}
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
                                                           gift_wrap_credits,promotional_rebates_refund])
    seller_fulfilled_selling_fees = spd.seller_fulfilled_selling_fees()
    FBA_selling_fees = spd.FBA_selling_fees()
    selling_fee_refund  = spd.selling_fee_refund()
    fba_transaction_fees  = spd.fba_transaction_fees()
    fba_transaction_fee_refunds   = spd.fba_transaction_fee_refunds()
    other_transaction_fees = spd.other_transaction_fees()
    other_transaction_fee_refunds = spd.other_transaction_fee_refunds()
    FBA_inventory_inbound_services_fees = spd.FBA_inventory_inbound_services_fees()

    Shipping_label_purchases = spd.Shipping_label_purchases()
    Shipping_label_refunds = spd.Shipping_label_refunds()
    carrier_shipping_label_adjustments = spd.carrier_shipping_label_adjustments()

    Service_fees = spd.Service_fees()
    Adjustments = spd.Adjustments()
    Refund_administration_fees  = spd.Refund_administration_fees()
    cost_of_advertising = spd.cost_of_advertising()
    refund_for_advertiser = spd.refund_for_advertiser()

    expense_subtotal_debits = spd.expenses_subtotal_debits([seller_fulfilled_selling_fees, FBA_selling_fees,
                                            fba_transaction_fees, other_transaction_fees,
                                            FBA_inventory_inbound_services_fees, Shipping_label_purchases,
                                            Service_fees, Refund_administration_fees,cost_of_advertising])
    expense_subtotal_credits = spd.expenses_subtotal_credits([selling_fee_refund,fba_transaction_fee_refunds,
                                                              other_transaction_fee_refunds,Shipping_label_refunds,
                                                              carrier_shipping_label_adjustments,Adjustments,
                                                              refund_for_advertiser])
    Income = spd.Income([income_subtotal_debits, income_subtotal_credits])
    summaries_income = spd.summaries_income([income_subtotal_debits, income_subtotal_credits])
    Exception = spd.Expenses([expense_subtotal_credits, expense_subtotal_debits])
    summaries_expenses = spd.summaries_expenses([expense_subtotal_credits, expense_subtotal_debits])
    Charges_to_credit_card = spd.charges_to_credit_card()
    transfers_to_bank_account_sum = spd.transfers_to_bank_account()
    Failed_transfers_to_bank_account = spd.failed_transfer_to_bank_account()
    Transfers = spd.Transfers([Charges_to_credit_card, transfers_to_bank_account_sum])
    subtotal_transfers  = spd.sub_credits_transfers([Charges_to_credit_card, Failed_transfers_to_bank_account])
    summaries_transfers = spd.summaries_transfers([Charges_to_credit_card, transfers_to_bank_account_sum])
    legal_name = spd.get_legal_name()

    return {"storename": storename, "product_sales": product_sales, "product_refund": product_refund,
            "legal_name": legal_name,
            "FBA_product_sales": FBA_product_sales, "FBA_product_refund": FBA_product_refund,
            "FBA_invenbry_credit": FBA_invenbry_credit, "shipping_credits": shipping_credits,
            "shipping_credits_refund": shipping_credits_refund, "gift_wrap_credits": gift_wrap_credits,
            "gift_wrap_credits_refund": gift_wrap_credits_refund, "promotional_rebates": promotional_rebates,
            "promotional_rebates_refund": promotional_rebates_refund,
            "a_to_z_guarantee_chaims": a_to_z_guarantee_chaims,
            "chargebacks": chargebacks, "income_subtotal_debits": income_subtotal_debits,
            "income_subtotal_credits": income_subtotal_credits,
            "seller_fulfilled_selling_fees": seller_fulfilled_selling_fees,
            "FBA_selling_fees": FBA_selling_fees, "selling_fee_refund": selling_fee_refund,
            "fba_transaction_fee_refunds": fba_transaction_fee_refunds, "fba_transaction_fees": fba_transaction_fees,
            "FBA_inventory_inbound_services_fees": FBA_inventory_inbound_services_fees,
            "Shipping_label_purchases": Shipping_label_purchases,
            "Shipping_label_refunds": Shipping_label_refunds,
            "carrier_shipping_label_adjustments": carrier_shipping_label_adjustments,
            "Service_fees": Service_fees, "Adjustments": Adjustments,
            "Refund_administration_fees": Refund_administration_fees,
            "cost_of_advertising": cost_of_advertising, "refund_for_advertiser": refund_for_advertiser,
            "expense_subtotal_debits": expense_subtotal_debits, "expense_subtotal_credits": expense_subtotal_credits,
            "Income": Income, "Exception": Exception, "Charges_to_credit_card": Charges_to_credit_card,
            "transfers_to_bank_account_sum": transfers_to_bank_account_sum,
            "Failed_transfers_to_bank_account": Failed_transfers_to_bank_account,
            "summaries_income": summaries_income, "summaries_expenses": summaries_expenses,
            "Transfers": Transfers, "summaries_transfers": summaries_transfers,
            "subtotal_transfers": subtotal_transfers,
            "begin_date_str": begin_date_str, "end_date_str": end_date_str}

def generate_dict_cc(**param_dict):
    year = param_dict.get("year", "")
    begin_date_str, end_date_str = param_dict.get("begin_date_str",""), param_dict.get("end_date_str", "")
    username, month= param_dict.get("username",""),param_dict.get("month","")
    if  begin_date_str and  end_date_str:
        begin_date = datetime.datetime.strptime(begin_date_str.strip(), "%b %d, %Y")
        end_date = datetime.datetime.strptime(end_date_str.strip(), "%b %d, %Y") + datetime.timedelta(days=1)  #date_time__range不包含最后一天
    else:
        begin_date, end_date = datetime.datetime.now(), datetime.datetime.now()
    parmas = {"month":month, "year":year, "begin_date":begin_date, "end_date":end_date}
    store = FilenameToStorename.objects.filter(email=username).first()

    timeRangeType = param_dict.get('timeRangeType','')
    product_sales_number = 0.0
    product_refund_number = 0.0
    FBA_product_sales_number = 0.0
    FBA_product_refund_number = 0.0
    FBA_invenbry_credit_number = 0.0
    shipping_credits_number = 0.0
    shipping_credits_refund_number = 0.0
    gift_wrap_credits_number = 0.0
    gift_wrap_credits_refund_number = 0.0
    promotional_rebates_number = 0.0
    promotional_rebates_refund_number = 0.0
    a_to_z_guarantee_chaims_number = 0.0
    chargebacks_number = 0.0
    income_subtotal_debits_number = 0.0
    income_subtotal_credits_number = 0.0
    seller_fulfilled_selling_fees_number = 0.0
    FBA_selling_fees_number = 0.0
    selling_fee_refund_number = 0.0
    fba_transaction_fee_number = 0.0
    fba_transaction_fee_refunds_number = 0.0
    other_transaction_fees_number = 0.0
    other_transaction_fee_refunds_number = 0.0
    FBA_inventory_inbound_services_fees_number = 0.0
    Shipping_label_purchases_number = 0.0
    Shipping_label_refunds_number = 0.0
    carrier_shipping_label_adjustments_number = 0.0
    Service_fees_number = 0.0
    Adjustments_number = 0.0
    Refund_administration_fees_number = 0.0
    cost_of_advertising_number = 0.0
    refund_for_advertiser_number = 0.0
    expense_subtotal_debits_number = 0.0
    expense_subtotal_credits_number = 0.0
    Income_number = 0.0
    summaries_income_number = 0.0
    Expenses_number = 0.0
    summaries_expenses_number = 0.0
    Charges_to_credit_card_number = 0.0
    transfers_to_bank_account_sum_number = 0.0
    Failed_transfers_to_bank_account_number = 0.0
    Transfers_number = 0.0
    subtotal_transfers_number = 0.0
    summaries_transfers_number = 0.0

    if timeRangeType == "Monthly":
        svm = StatementViewMonth.objects.filter(year=year,month=month,serial_number=store.serial_number).first()
        storename = store.storename
        product_sales_number = number_format(svm.product_sales)
        product_sales = {'number_length': oredits_number_len(product_sales_number),
                         'number': product_sales_number}

        product_refund_number = number_format(svm.product_refund)
        product_refund = {'number_length': debits_number_len(product_refund_number),
                          'number': product_refund_number}

        FBA_product_sales_number = number_format(svm.FBA_product_sales)
        FBA_product_sales = {'number_length': oredits_number_len(FBA_product_sales_number),
                             'number': FBA_product_sales_number}

        FBA_product_refund_number = number_format(svm.FBA_product_refund)
        FBA_product_refund = {'number_length': debits_number_len(FBA_product_refund_number),
                              'number': FBA_product_refund_number}

        FBA_invenbry_credit_number = number_format(svm.FBA_invenbry_credit)
        FBA_invenbry_credit = {'number_length': oredits_number_len(FBA_invenbry_credit_number),
                               'number':FBA_invenbry_credit_number }

        shipping_credits_number = number_format(svm.shipping_credits)
        shipping_credits = {'number_length': oredits_number_len(shipping_credits_number),
                            'number':shipping_credits_number }

        shipping_credits_refund_number = number_format(svm.shipping_credits_refund)
        shipping_credits_refund = {'number_length': debits_number_len(shipping_credits_refund_number),
                                   'number': shipping_credits_refund_number}

        gift_wrap_credits_number = number_format(svm.gift_wrap_credits)
        gift_wrap_credits = {'number_length': oredits_number_len(gift_wrap_credits_number),
                             'number': gift_wrap_credits_number}

        gift_wrap_credits_refund_number = number_format(svm.gift_wrap_credits_refund)
        gift_wrap_credits_refund = {'number_length': debits_number_len(gift_wrap_credits_refund_number),
                                    'number': gift_wrap_credits_refund_number}

        promotional_rebates_number = number_format(svm.promotional_rebates)
        promotional_rebates = {'number_length': debits_number_len(promotional_rebates_number),
                               'number': promotional_rebates_number}

        promotional_rebates_refund_number = number_format(svm.promotional_rebates_refund)
        promotional_rebates_refund = {'number_length': oredits_number_len(promotional_rebates_refund_number),
                                      'number': promotional_rebates_refund_number}

        a_to_z_guarantee_chaims_number = number_format(svm.a_to_z_guarantee_chaims)
        a_to_z_guarantee_chaims = {'number_length': debits_number_len(a_to_z_guarantee_chaims_number),
                                   'number': a_to_z_guarantee_chaims_number}

        chargebacks_number = number_format(svm.chargebacks)
        chargebacks = {'number_length': debits_number_len(chargebacks_number),
                       'number': chargebacks_number}

        income_subtotal_debits_number = number_format(svm.income_subtotal_debits)
        income_subtotal_debits = {'number_length': debits_number_len(income_subtotal_debits_number),
                                  'number': income_subtotal_debits_number}

        income_subtotal_credits_number = number_format(svm.income_subtotal_credits)
        income_subtotal_credits = {'number_length': oredits_number_len(income_subtotal_credits_number),
                                   'number': income_subtotal_credits_number}

        seller_fulfilled_selling_fees_number = number_format(svm.seller_fulfilled_selling_fees)
        seller_fulfilled_selling_fees = {'number_length': expense_debits_len(seller_fulfilled_selling_fees_number),
                                         'number': seller_fulfilled_selling_fees_number}

        FBA_selling_fees_number = number_format(svm.FBA_selling_fees)
        FBA_selling_fees = {'number_length': expense_debits_len(FBA_selling_fees_number),
                            'number': FBA_selling_fees_number}

        selling_fee_refund_number = number_format(svm.selling_fee_refund)
        selling_fee_refund = {'number_length': expend_credicts_len(selling_fee_refund_number),
                              'number': selling_fee_refund_number}

        fba_transaction_fee_number =  number_format(svm.fba_transaction_fees)
        fba_transaction_fees = {'number_length': expense_debits_len(fba_transaction_fee_number),
                                'number':fba_transaction_fee_number}

        fba_transaction_fee_refunds_number =  number_format(svm.fba_transaction_fee_refunds)
        fba_transaction_fee_refunds = {'number_length': expend_credicts_len(fba_transaction_fee_refunds_number),
                                       'number':fba_transaction_fee_refunds_number}

        other_transaction_fees_number = number_format(svm.other_transaction_fees)
        other_transaction_fees = {'number_length': expense_debits_len(other_transaction_fees_number),
                                  'number': other_transaction_fees_number}

        other_transaction_fee_refunds_number= number_format(svm.other_transaction_fee_refunds)
        other_transaction_fee_refunds = {'number_length': expend_credicts_len(other_transaction_fee_refunds_number),
                                         'number': other_transaction_fee_refunds_number}

        FBA_inventory_inbound_services_fees_number = number_format(svm.FBA_inventory_inbound_services_fees)
        FBA_inventory_inbound_services_fees = {'number_length': expense_debits_len(FBA_inventory_inbound_services_fees_number),
                                               'number':FBA_inventory_inbound_services_fees_number }

        Shipping_label_purchases_number = number_format(svm.Shipping_label_purchases)
        Shipping_label_purchases = {'number_length': expense_debits_len(Shipping_label_purchases_number),
                                    'number':Shipping_label_purchases_number }

        Shipping_label_refunds_number = number_format(svm.Shipping_label_refunds)
        Shipping_label_refunds = {'number_length': expend_credicts_len(Shipping_label_refunds_number),
                                  'number': Shipping_label_refunds_number}

        carrier_shipping_label_adjustments_number = number_format(svm.carrier_shipping_label_adjustments)
        carrier_shipping_label_adjustments = {'number_length': expend_credicts_len(carrier_shipping_label_adjustments_number),
                                              'number': carrier_shipping_label_adjustments_number}

        Service_fees_number = number_format(svm.Service_fees)
        Service_fees = {'number_length': expense_debits_len(Service_fees_number),
                        'number':Service_fees_number}

        Adjustments_number = number_format(svm.Adjustments)
        Adjustments = {'number_length': expend_credicts_len(Adjustments_number),
                       'number':Adjustments_number}

        Refund_administration_fees_number = number_format(svm.Refund_administration_fees)
        Refund_administration_fees = {'number_length': expense_debits_len(Refund_administration_fees_number),
                                      'number': Refund_administration_fees_number}

        cost_of_advertising_number = number_format(svm.cost_of_advertising)
        cost_of_advertising = {'number_length': expense_debits_len(cost_of_advertising_number),
                               'number': cost_of_advertising_number}

        refund_for_advertiser_number =  number_format(svm.refund_for_advertiser)
        refund_for_advertiser = {'number_length': expend_credicts_len(refund_for_advertiser_number),
                                 'number':refund_for_advertiser_number}

        expense_subtotal_debits_number = number_format(svm.expense_subtotal_debits)
        expense_subtotal_debits = {'number_length': expense_debits_len(expense_subtotal_debits_number),
                                   'number': expense_subtotal_debits_number}

        expense_subtotal_credits_number = number_format(svm.expense_subtotal_credits)
        expense_subtotal_credits = {'number_length': expend_credicts_len(expense_subtotal_credits_number),
                                    'number': expense_subtotal_credits_number}

        Income_number = number_format(svm.Income)
        Income = {'number_length': Income_len(Income_number),
                  'number':Income_number}

        summaries_income_number = number_format(svm.summaries_income)
        summaries_income = {'number_length': expend_credicts_len(summaries_income_number),
                            'number':summaries_income_number }

        Expenses_number = number_format(svm.Expenses)
        Expenses = {'number_length': Expenses_len(Expenses_number),
                    'number': Expenses_number}

        summaries_expenses_number = number_format(svm.summaries_expenses)
        summaries_expenses = {'number_length': expend_credicts_len(summaries_expenses_number),
                              'number': summaries_expenses_number}

        Charges_to_credit_card_number = number_format(svm.Charges_to_credit_card)
        Charges_to_credit_card = {'number_length': oredits_number_len(Charges_to_credit_card_number),
                                  'number':Charges_to_credit_card_number}

        transfers_to_bank_account_sum_number = number_format(svm.transfers_to_bank_account_sum)
        transfers_to_bank_account_sum = {'number_length': debits_number_len(transfers_to_bank_account_sum_number),
                                         'number': transfers_to_bank_account_sum_number}

        Failed_transfers_to_bank_account_number = number_format(svm.Failed_transfers_to_bank_account)
        Failed_transfers_to_bank_account = {'number_length': debits_number_len(Failed_transfers_to_bank_account_number),
                                            'number': Failed_transfers_to_bank_account_number}

        Transfers_number = number_format(svm.Transfers)
        Transfers = {'number_length': Income_len(Transfers_number),
                     'number': Transfers_number}

        subtotal_transfers_number = number_format(svm.subtotal_transfers)
        subtotal_transfers = {'number_length': oredits_number_len(subtotal_transfers_number),
                              'number': subtotal_transfers_number}

        summaries_transfers_number = number_format(svm.summaries_transfers)
        summaries_transfers = {'number_length': expend_credicts_len(summaries_transfers_number),
                               'number':summaries_transfers_number}
        legal_name = store.manager
    else:
        svms = StatementViewMonth.objects.filter(year=year, serial_number=store.serial_number)

        for svm in svms:
            product_sales_number += str_to_float(svm.product_sales)

            product_refund_number += str_to_float(svm.product_refund)

            FBA_product_sales_number += str_to_float(svm.FBA_product_sales)

            FBA_product_refund_number += str_to_float(svm.FBA_product_refund)

            FBA_invenbry_credit_number += str_to_float(svm.FBA_invenbry_credit)

            shipping_credits_number += str_to_float(svm.shipping_credits)

            shipping_credits_refund_number += str_to_float(svm.shipping_credits_refund)

            gift_wrap_credits_number += str_to_float(svm.gift_wrap_credits)

            gift_wrap_credits_refund_number += str_to_float(svm.gift_wrap_credits_refund)

            promotional_rebates_number += str_to_float(svm.promotional_rebates)

            promotional_rebates_refund_number += str_to_float(svm.promotional_rebates_refund)

            a_to_z_guarantee_chaims_number += str_to_float(svm.a_to_z_guarantee_chaims)

            chargebacks_number += str_to_float(svm.chargebacks)

            income_subtotal_debits_number += str_to_float(svm.income_subtotal_debits)

            income_subtotal_credits_number += str_to_float(svm.income_subtotal_credits)

            seller_fulfilled_selling_fees_number += str_to_float(svm.seller_fulfilled_selling_fees)

            FBA_selling_fees_number += str_to_float(svm.FBA_selling_fees)

            selling_fee_refund_number += str_to_float(svm.selling_fee_refund)

            fba_transaction_fee_number += str_to_float(svm.fba_transaction_fees)

            fba_transaction_fee_refunds_number += str_to_float(svm.fba_transaction_fee_refunds)

            other_transaction_fees_number += str_to_float(svm.other_transaction_fees)

            other_transaction_fee_refunds_number += str_to_float(svm.other_transaction_fee_refunds)

            FBA_inventory_inbound_services_fees_number += str_to_float(svm.FBA_inventory_inbound_services_fees)

            Shipping_label_purchases_number += str_to_float(svm.Shipping_label_purchases)

            Shipping_label_refunds_number += str_to_float(svm.Shipping_label_refunds)

            carrier_shipping_label_adjustments_number += str_to_float(svm.carrier_shipping_label_adjustments)

            Service_fees_number += str_to_float(svm.Service_fees)

            Adjustments_number += str_to_float(svm.Adjustments)

            Refund_administration_fees_number += str_to_float(svm.Refund_administration_fees)

            cost_of_advertising_number += str_to_float(svm.cost_of_advertising)

            refund_for_advertiser_number += str_to_float(svm.refund_for_advertiser)

            expense_subtotal_debits_number += str_to_float(svm.expense_subtotal_debits)

            expense_subtotal_credits_number += str_to_float(svm.expense_subtotal_credits)

            Income_number += str_to_float(svm.Income)

            summaries_income_number += str_to_float(svm.summaries_income)

            Expenses_number += str_to_float(svm.Expenses)

            summaries_expenses_number += str_to_float(svm.summaries_expenses)

            Charges_to_credit_card_number += str_to_float(svm.Charges_to_credit_card)

            transfers_to_bank_account_sum_number += str_to_float(svm.transfers_to_bank_account_sum)

            Failed_transfers_to_bank_account_number += str_to_float(svm.Failed_transfers_to_bank_account)

            Transfers_number += str_to_float(svm.Transfers)

            subtotal_transfers_number += str_to_float(svm.subtotal_transfers)

            summaries_transfers_number += str_to_float(svm.summaries_transfers)
        storename = store.storename
        product_sales_number = number_format(product_sales_number)
        product_sales = {'number_length': oredits_number_len(product_sales_number),
                         'number': product_sales_number}

        product_refund_number = number_format(product_refund_number)
        product_refund = {'number_length': debits_number_len(product_refund_number),
                          'number': product_refund_number}

        FBA_product_sales_number = number_format(FBA_product_sales_number)
        FBA_product_sales = {'number_length': oredits_number_len(FBA_product_sales_number),
                             'number': FBA_product_sales_number}

        FBA_product_refund_number = number_format(FBA_product_refund_number)
        FBA_product_refund = {'number_length': debits_number_len(FBA_product_refund_number),
                              'number': FBA_product_refund_number}

        FBA_invenbry_credit_number = number_format(FBA_invenbry_credit_number)
        FBA_invenbry_credit = {'number_length': oredits_number_len(FBA_invenbry_credit_number),
                               'number': FBA_invenbry_credit_number}

        shipping_credits_number = number_format(shipping_credits_number)
        shipping_credits = {'number_length': oredits_number_len(shipping_credits_number),
                            'number': shipping_credits_number}

        shipping_credits_refund_number = number_format(shipping_credits_refund_number)
        shipping_credits_refund = {'number_length': debits_number_len(shipping_credits_refund_number),
                                   'number': shipping_credits_refund_number}

        gift_wrap_credits_number = number_format(gift_wrap_credits_number)
        gift_wrap_credits = {'number_length': oredits_number_len(gift_wrap_credits_number),
                             'number': gift_wrap_credits_number}

        gift_wrap_credits_refund_number = number_format(gift_wrap_credits_refund_number)
        gift_wrap_credits_refund = {'number_length': debits_number_len(gift_wrap_credits_refund_number),
                                    'number': gift_wrap_credits_refund_number}

        promotional_rebates_number = number_format(promotional_rebates_number)
        promotional_rebates = {'number_length': debits_number_len(promotional_rebates_number),
                               'number': promotional_rebates_number}

        promotional_rebates_refund_number = number_format(promotional_rebates_refund_number)
        promotional_rebates_refund = {'number_length': oredits_number_len(promotional_rebates_refund_number),
                                      'number': promotional_rebates_refund_number}

        a_to_z_guarantee_chaims_number = number_format(a_to_z_guarantee_chaims_number)
        a_to_z_guarantee_chaims = {'number_length': debits_number_len(a_to_z_guarantee_chaims_number),
                                   'number': a_to_z_guarantee_chaims_number}

        chargebacks_number = number_format(chargebacks_number)
        chargebacks = {'number_length': debits_number_len(chargebacks_number),
                       'number': chargebacks_number}

        income_subtotal_debits_number = number_format(income_subtotal_debits_number)
        income_subtotal_debits = {'number_length': debits_number_len(income_subtotal_debits_number),
                                  'number': income_subtotal_debits_number}

        income_subtotal_credits_number = number_format(income_subtotal_credits_number)
        income_subtotal_credits = {'number_length': oredits_number_len(income_subtotal_credits_number),
                                   'number': income_subtotal_credits_number}

        seller_fulfilled_selling_fees_number = number_format(seller_fulfilled_selling_fees_number)
        seller_fulfilled_selling_fees = {'number_length': expense_debits_len(seller_fulfilled_selling_fees_number),
                                         'number': seller_fulfilled_selling_fees_number}

        FBA_selling_fees_number = number_format(FBA_selling_fees_number)
        FBA_selling_fees = {'number_length': expense_debits_len(FBA_selling_fees_number),
                            'number': FBA_selling_fees_number}

        selling_fee_refund_number = number_format(selling_fee_refund_number)
        selling_fee_refund = {'number_length': expend_credicts_len(selling_fee_refund_number),
                              'number': selling_fee_refund_number}

        fba_transaction_fee_number = number_format(fba_transaction_fee_number)
        fba_transaction_fees = {'number_length': expense_debits_len(fba_transaction_fee_number),
                                'number': fba_transaction_fee_number}

        fba_transaction_fee_refunds_number = number_format(fba_transaction_fee_refunds_number)
        fba_transaction_fee_refunds = {'number_length': expend_credicts_len(fba_transaction_fee_refunds_number),
                                       'number': fba_transaction_fee_refunds_number}

        other_transaction_fees_number = number_format(other_transaction_fees_number)
        other_transaction_fees = {'number_length': expense_debits_len(other_transaction_fees_number),
                                  'number': other_transaction_fees_number}

        other_transaction_fee_refunds_number = number_format(other_transaction_fee_refunds_number)
        other_transaction_fee_refunds = {'number_length': expend_credicts_len(other_transaction_fee_refunds_number),
                                         'number': other_transaction_fee_refunds_number}

        FBA_inventory_inbound_services_fees_number = number_format(FBA_inventory_inbound_services_fees_number)
        FBA_inventory_inbound_services_fees = {
            'number_length': expense_debits_len(FBA_inventory_inbound_services_fees_number),
            'number': FBA_inventory_inbound_services_fees_number}

        Shipping_label_purchases_number = number_format(Shipping_label_purchases_number)
        Shipping_label_purchases = {'number_length': expense_debits_len(Shipping_label_purchases_number),
                                    'number': Shipping_label_purchases_number}

        Shipping_label_refunds_number = number_format(Shipping_label_refunds_number)
        Shipping_label_refunds = {'number_length': expend_credicts_len(Shipping_label_refunds_number),
                                  'number': Shipping_label_refunds_number}

        carrier_shipping_label_adjustments_number = number_format(carrier_shipping_label_adjustments_number)
        carrier_shipping_label_adjustments = {
            'number_length': expend_credicts_len(carrier_shipping_label_adjustments_number),
            'number': carrier_shipping_label_adjustments_number}

        Service_fees_number = number_format(Service_fees_number)
        Service_fees = {'number_length': expense_debits_len(Service_fees_number),
                        'number': Service_fees_number}

        Adjustments_number = number_format(Adjustments_number)
        Adjustments = {'number_length': expend_credicts_len(Adjustments_number),
                       'number': Adjustments_number}

        Refund_administration_fees_number = number_format(Refund_administration_fees_number)
        Refund_administration_fees = {'number_length': expense_debits_len(Refund_administration_fees_number),
                                      'number': Refund_administration_fees_number}

        cost_of_advertising_number = number_format(cost_of_advertising_number)
        cost_of_advertising = {'number_length': expense_debits_len(cost_of_advertising_number),
                               'number': cost_of_advertising_number}

        refund_for_advertiser_number = number_format(refund_for_advertiser_number)
        refund_for_advertiser = {'number_length': expend_credicts_len(refund_for_advertiser_number),
                                 'number': refund_for_advertiser_number}

        expense_subtotal_debits_number = number_format(expense_subtotal_debits_number)
        expense_subtotal_debits = {'number_length': expense_debits_len(expense_subtotal_debits_number),
                                   'number': expense_subtotal_debits_number}

        expense_subtotal_credits_number = number_format(expense_subtotal_credits_number)
        expense_subtotal_credits = {'number_length': expend_credicts_len(expense_subtotal_credits_number),
                                    'number': expense_subtotal_credits_number}

        Income_number = number_format(Income_number)
        Income = {'number_length': Income_len(Income_number),
                  'number': Income_number}

        summaries_income_number = number_format(summaries_income_number)
        summaries_income = {'number_length': expend_credicts_len(summaries_income_number),
                            'number': summaries_income_number}

        Expenses_number = number_format(Expenses_number)
        Expenses = {'number_length': Expenses_len(Expenses_number),
                    'number': Expenses_number}

        summaries_expenses_number = number_format(summaries_expenses_number)
        summaries_expenses = {'number_length': expend_credicts_len(summaries_expenses_number),
                              'number': summaries_expenses_number}

        Charges_to_credit_card_number = number_format(Charges_to_credit_card_number)
        Charges_to_credit_card = {'number_length': oredits_number_len(Charges_to_credit_card_number),
                                  'number': Charges_to_credit_card_number}

        transfers_to_bank_account_sum_number = number_format(transfers_to_bank_account_sum_number)
        transfers_to_bank_account_sum = {'number_length': debits_number_len(transfers_to_bank_account_sum_number),
                                         'number': transfers_to_bank_account_sum_number}

        Failed_transfers_to_bank_account_number = number_format(Failed_transfers_to_bank_account_number)
        Failed_transfers_to_bank_account = {'number_length': debits_number_len(Failed_transfers_to_bank_account_number),
                                            'number': Failed_transfers_to_bank_account_number}

        Transfers_number = number_format(Transfers_number)
        Transfers = {'number_length': Income_len(Transfers_number),
                     'number': Transfers_number}

        subtotal_transfers_number = number_format(subtotal_transfers_number)
        subtotal_transfers = {'number_length': oredits_number_len(subtotal_transfers_number),
                              'number': subtotal_transfers_number}

        summaries_transfers_number = number_format(summaries_transfers_number)
        summaries_transfers = {'number_length': expend_credicts_len(summaries_transfers_number),
                               'number': summaries_transfers_number}
        legal_name = store.manager

    return {"storename":storename,"legal_name": legal_name,"begin_date_str": begin_date_str, "end_date_str":end_date_str,
            "summaries_income": summaries_income,
            "summaries_expenses": summaries_expenses,
            "summaries_sales_tax":{"number":0},
            "summaries_transfers": summaries_transfers,
            "product_sales":product_sales,"product_refund":product_refund,
            "FBA_product_sales":FBA_product_sales, "FBA_product_refund":FBA_product_refund,
            "FBA_invenbry_credit":FBA_invenbry_credit,
            "shipping_credits":shipping_credits,"shipping_credits_refund":shipping_credits_refund,
            "gift_wrap_credits":gift_wrap_credits,"gift_wrap_credits_refund":gift_wrap_credits_refund,
            "promotional_rebates":promotional_rebates,"promotional_rebates_refund":promotional_rebates_refund,
            "a_to_z_guarantee_chaims":a_to_z_guarantee_chaims,"chargebacks":chargebacks,
            "income_subtotal_debits":income_subtotal_debits,"income_subtotal_credits":income_subtotal_credits,

            "seller_fulfilled_selling_fees":seller_fulfilled_selling_fees,
            "FBA_selling_fees":FBA_selling_fees,"selling_fee_refund":selling_fee_refund,
            "fba_transaction_fees":fba_transaction_fees,"fba_transaction_fee_refunds":fba_transaction_fee_refunds,
            "other_transaction_fees": other_transaction_fees, "other_transaction_fee_refunds": other_transaction_fee_refunds,
            "FBA_inventory_inbound_services_fees":FBA_inventory_inbound_services_fees,
            "Shipping_label_purchases":Shipping_label_purchases,"Shipping_label_refunds":Shipping_label_refunds,
            "carrier_shipping_label_adjustments":carrier_shipping_label_adjustments,
            "Service_fees":Service_fees,"Refund_administration_fees":Refund_administration_fees,"Adjustments":Adjustments,
            "cost_of_advertising":cost_of_advertising, "refund_for_advertiser":refund_for_advertiser,
            "expense_subtotal_debits":expense_subtotal_debits, "expense_subtotal_credits":expense_subtotal_credits,

            "transfers_to_bank_account_sum": transfers_to_bank_account_sum,
            "Failed_transfers_to_bank_account": Failed_transfers_to_bank_account,
            "Charges_to_credit_card": Charges_to_credit_card,
            "subtotal_transfers":subtotal_transfers,
            "Income": Income, "Exception": Expenses, "Transfers": Transfers, "Sales_Tax": 0}





def create_pdf_from_html(**params):
    params_file = params.get("filename", "")
    if params_file:
        pdf_filename = params_file
    else:
        pdf_filename = "output.pdf"
    base_dir = settings.BASE_DIR
    generate_dir = settings.GENERATE_REPORT_PATH
    pdf_dir = os.path.join(base_dir, "center/templates/pdf_hml/")
    filename = os.path.join(pdf_dir,"2017Liu_MonthlySummary.html")
    pdf_html_str = open(filename).read()
    t = Template(pdf_html_str)
    # g_dict = generate_dict(**params)
    g_dict = generate_dict_cc(**params)
    c = Context(g_dict)
    result_html = t.render(c)
    result_filename = os.path.join(pdf_dir, "result_pdf.html")
    output_file = os.path.join(generate_dir, pdf_filename)
    try:
        with open(result_filename, "w") as f:
            f.write(result_html)
    except Exception, e:
        print e
    try:
        output_file = html_to_pdf(result_filename, output_file)
        # os.system("wkhtmltopdf %s %s"%(result_filename, output_file))
    except Exception,e :
        output_file = ""
        print "html to pdf error %s"%str(e)

    return output_file
