#!/usr/bin/env python
# encoding:utf-8

from django.db.models import  Sum

from django.db.models import Q
from manageApp.models import StatementView
from manageApp.models import FilenameToStorename



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

    def product_sales(self):
        print self.serial_number
        query_select = Q(serial_number=self.serial_number, type="Order")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            product_sale_query_dict = StatementView.objects.filter(query_select).values("product_sales", "other").aggregate(Sum("product_sales"),Sum("other"))
        except Exception, e:
            product_sale_query_dict = {}
        if product_sale_query_dict.get("product_sales__sum") and product_sale_query_dict.get("other__sum"):
            product_sale_sum = product_sale_query_dict.get("product_sales__sum", 0) + product_sale_query_dict.get("other__sum", 0)
        else:
            product_sale_sum = 0
        product_sale_sum = format(product_sale_sum, ",")
        product_sale_html_sum = oredits_number_len(product_sale_sum)
        return {"number_length": product_sale_html_sum, "number": product_sale_sum}


    def product_refund(self):
        query_select = Q(serial_number=self.serial_number, type="Refund")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            product_refund_query_dict = StatementView.objects.filter(query_select).values("product_sales", "other").aggregate(Sum("product_sales"),Sum("other"))
        except Exception, e:
            product_refund_query_dict = {}
        if product_refund_query_dict.get("product_sales__sum") and product_refund_query_dict.get("other__sum"):
            product_refund_sum = product_refund_query_dict.get("product_sales__sum") + product_refund_query_dict.get("other__sum")
        else:
            product_refund_sum = 0
        product_refund_sum = format(product_refund_sum, ",")
        return {"number_length": debits_number_len(product_refund_sum), "number": product_refund_sum}


    def FBA_product_sales(self):
        print self.serial_number
        query_select = Q(serial_number=self.serial_number, type="Order", fulfillment="Amazon")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            product_sale_query_dict = StatementView.objects.filter(query_select).values("product_sales", "other").aggregate(Sum("product_sales"),Sum("other"))
        except Exception, e:
            product_sale_query_dict = {}
        if product_sale_query_dict.get("product_sales__sum") and product_sale_query_dict.get("other__sum"):
            product_sale_sum = product_sale_query_dict.get("product_sales__sum", 0) + product_sale_query_dict.get("other__sum", 0)
        else:
            product_sale_sum = 0
        product_sale_sum = format(product_sale_sum, ",")
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
        if product_refund_query_dict.get("product_sales__sum") and product_refund_query_dict.get("other__sum"):
            product_refund_sum = product_refund_query_dict.get("product_sales__sum") + product_refund_query_dict.get("other__sum")
        else:
            product_refund_sum = 0
        product_refund_sum = format(product_refund_sum, ",")
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
        if inventory_credit_dict.get("total__sum"):
            products_credit_sum = inventory_credit_dict.get("total__sum", 0)
        else:
            products_credit_sum = 0
        products_credit_sum = products_credit_sum - 0 # expense中的Adjustments"一般为0
        products_credit_sum = format(products_credit_sum, ",")
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
        if shipping_credits_dict.get("shipping_credits__sum", ""):
            shipping_credits_sum = shipping_credits_dict.get("shipping_credits__sum", 0)
        else:
            shipping_credits_sum = 0
        shipping_credits_sum = format(shipping_credits_sum, ",")
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
        if shipping_credits_refund_dict.get("shipping_credits__sum", ""):
            shipping_credits_refund_sum = shipping_credits_refund_dict.get("shipping_credits__sum", 0)
        else:
            shipping_credits_refund_sum = 0
        shipping_credits_refund_sum = format(shipping_credits_refund_sum, ",")
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
        if gift_wrap_credits_dict.get("gift_wrap_credits__sum"):
            gift_wrap_credits_sum = gift_wrap_credits_dict.get("gift_wrap_credits__sum", 0)
        else:
            gift_wrap_credits_sum = 0
        gift_wrap_credits_sum = format(gift_wrap_credits_sum, ",")
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
        if gift_wrap_credits_refund_dict.get("gift_wrap_credits__sum"):
            gift_wrap_credits_refund_sum = gift_wrap_credits_refund_dict.get("gift_wrap_credits__sum", 0)
        else:
            gift_wrap_credits_refund_sum = 0
        gift_wrap_credits_sum = format(gift_wrap_credits_refund_sum, ",")
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
        if promotional_rebates_dict.get("promotional_rebates__sum"):
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
        if promotional_rebates_refund_dict.get("promotional_rebates__sum"):
            promotional_rebates_sum = promotional_rebates_refund_dict.get("promotional_rebates__sum", 0)
        else:
            promotional_rebates_sum = 0
        promotional_rebates_sum = format(promotional_rebates_sum, ",")
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
        if a_to_z_gurantee_claim_dict.get("total__sum"):
            a_to_z_gurantee_claim_sum = a_to_z_gurantee_claim_dict.get("total__sum", 0)
        else:
            a_to_z_gurantee_claim_sum = 0
        a_to_z_gurantee_claim_sum = format(a_to_z_gurantee_claim_sum, ",")
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
        if chargebacks_dict.get("total__sum"):
            chargebacks_sum = chargebacks_dict.get("total__sum", 0)
        else:
            chargebacks_sum = 0
        chargebacks_sum = format(chargebacks_sum, ",")
        return {"number_length": debits_number_len(chargebacks_sum), "number": chargebacks_sum}


    def income_subtotal_debits(self, subtotal_list):
        income_subtotal_debits_number = sum([float(i.get("number", '0').replace(",", "")) for i in subtotal_list])
        income_subtotal_debits_number = format(income_subtotal_debits_number,",")
        return {"number_length": debits_number_len(income_subtotal_debits_number), "number": income_subtotal_debits_number}

    def income_subtotal_credits(self, subtotal_list):
        income_subtotal_debits_number = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        income_subtotal_debits_number = format(income_subtotal_debits_number,",")
        return  {"number_length": oredits_number_len(income_subtotal_debits_number), "number": income_subtotal_debits_number}


    #----------------------  Expenses   --------------------------
    def seller_fulfilled_selling_fees(self):
        """ type(Order) + R列数据"""
        query_select = Q(serial_number = self.serial_number, type="Order")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            seller_fulfilled_selling_fees_dict = StatementView.objects.filter(query_select).values("selling_fees").aggregate(Sum("selling_fees"))
        except Exception, e:
            seller_fulfilled_selling_fees_dict = {}
        if seller_fulfilled_selling_fees_dict.get("selling_fees__sum"):
            seller_fulfilled_selling_fees_sum = seller_fulfilled_selling_fees_dict.get("selling_fees__sum", 0)
        else:
            seller_fulfilled_selling_fees_sum = 0
        seller_fulfilled_selling_fees_sum = format(seller_fulfilled_selling_fees_sum, ",")
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
        if FBA_selling_fees_dict.get("selling_fees__sum"):
            FBA_selling_fees_sum = FBA_selling_fees_dict.get("selling_fees__sum", 0)
        else:
            FBA_selling_fees_sum = 0
        FBA_selling_fees_sum = format(FBA_selling_fees_sum, ",")
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
        if selling_fee_refund_dict.get("selling_fees__sum"):
            selling_fee_refund_sum = selling_fee_refund_dict.get("selling_fees__sum", 0)
        else:
            selling_fee_refund_sum = 0
        selling_fee_refund_sum = format(selling_fee_refund_sum, ",")
        return {"number_length": expend_credicts_len(selling_fee_refund_sum), "number":selling_fee_refund_sum}


    def fba_transaction_fees(self):
        """ tyoe(Order)对应的S列 """
        query_select = Q(serial_number = self.serial_number, type="Order")
        if self.begin_date and self.end_date:
            query_select = query_select & Q(date_time__range=(self.begin_date, self.end_date))
        try:
            fba_trasaction_fees_dict = StatementView.objects.filter(query_select).values("fba_fees").aggregate(Sum("fba_fees"))
        except Exception, e:
            fba_trasaction_fees_dict = {}
        if fba_trasaction_fees_dict.get("fba_fees__sum"):
            fba_trasaction_fees_sum = fba_trasaction_fees_dict.get("fba_fees__sum", 0)
        else:
            fba_trasaction_fees_sum = 0
        fba_trasaction_fees_sum = format(fba_trasaction_fees_sum, ",")
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
        fba_transaction_fee_refund_sum = format(fba_transaction_fee_refund_sum, ",")
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
        other_transaction_fee_sum = format(other_transaction_fee_sum, ",")
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
        other_transaction_fee_refund_sum = format(other_transaction_fee_refund_sum, ",")
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
        if FBA_inventory_inbound_services_dict.get("total__sum"):
            FBA_inventory_inbound_services_sum = FBA_inventory_inbound_services_dict.get("total__sum", 0)
        else:
            FBA_inventory_inbound_services_sum = 0
        FBA_inventory_inbound_services_sum =  format(FBA_inventory_inbound_services_sum, ",")
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
        query_select = Q(serial_number=self.serial_number, type="Service Fee")
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
        service_fees_sum = format(service_fees_sum, ",")
        return {"number_length": expense_debits_len(service_fees_sum), "number": service_fees_sum}


    def Refund_administration_fees(self):
        """ 这项不变 """
        refund_administration_fees_sum = -12
        return {"number_length":expense_debits_len(refund_administration_fees_sum), "number":refund_administration_fees_sum}

    def Adjustments(self):
        adjuestments_sum = 0
        return {"number_length": expend_credicts_len(adjuestments_sum), "number": adjuestments_sum}

    def cost_of_advertising(self):
        cost_of_advertising_sum = 0
        return {"number_length": expense_debits_len(cost_of_advertising_sum), "number": cost_of_advertising_sum}


    def refund_for_advertiser(self):
        refund_for_advertiser_sum = 0
        return {"number_length": expend_credicts_len(refund_for_advertiser_sum), "number": refund_for_advertiser_sum}

    def expenses_subtotal_debits(self, subtotal_list):
        """ expenses debits  total """
        income_subtotal_debits_number = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        income_subtotal_debits_number = format(income_subtotal_debits_number, ",")
        return {"number_length": expense_debits_len(income_subtotal_debits_number), "number": income_subtotal_debits_number}

    def expenses_subtotal_credits(self, subtotal_list):
        """ expenses credits  total """
        income_subtotal_debits_number = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        income_subtotal_debits_number = format(income_subtotal_debits_number, ",")
        return {"number_length": expend_credicts_len(income_subtotal_debits_number), "number": income_subtotal_debits_number}


    def Income(self, subtotal_list):
        Income_sum = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        Income_sum = format(Income_sum, ",")
        return {"number_length":Income_len(Income_sum), "number": Income_sum}

    def Expenses(self, subtotal_list):
        expenses_number = sum([float(str(i.get("number", '0')).replace(",", "")) for i in subtotal_list])
        expenses_number = format(expenses_number, ",")
        return {"number_length": Expenses_len(expenses_number), "number": expenses_number}

