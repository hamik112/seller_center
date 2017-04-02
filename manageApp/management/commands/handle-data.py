# -*- coding: utf-8 -*-
import sys
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'SellerCenter.settings'
django.setup()
print os.environ.get('DJANGO_SETTINGS_MODULE')

from django.core.management.base import BaseCommand
import MySQLdb
from datetime import datetime,timedelta
import dateutil
import calendar

from SellerCenter.settings import DATABASES
from manageApp.models import FilenameToStorename,StatementViewMonth

reload(sys)
sys.setdefaultencoding('utf-8')

mysql_setting = DATABASES.get('default')
class Command(BaseCommand):
    def handle(self, *args, **options):
        print "start"
        handle_data(*args)



def handle_data(*args):
    print '++++++++++++++++++++++++++++++++++++'
    conn = MySQLdb.connect(
        host=mysql_setting.get('HOST') if mysql_setting.get('HOST') else '127.0.0.1',
        port=int(mysql_setting.get('PORT')) if mysql_setting.get('PORT') else 3306,
        user=mysql_setting.get('USER'),
        passwd=mysql_setting.get('PASSWORD'),
        db=mysql_setting.get('NAME'),
        charset="utf8"
    )
    print mysql_setting.get('HOST')
    print mysql_setting.get('PORT')
    print mysql_setting.get('USER')
    print mysql_setting.get('PASSWORD')
    print mysql_setting.get('NAME')
    cur = conn.cursor()
    stores  = FilenameToStorename.objects.filter(serial_number='ABC-58')
    Shipping_label_purchases = 0
    Shipping_label_refunds = 0
    carrier_shipping_label_adjustments = 0
    Adjustments = 0
    Refund_administration_fees = 0
    refund_for_advertiser = 0
    Failed_transfers_to_bank_account = 0
    now_data = datetime.now()
    for store in stores:
        serial_number = store.serial_number
        start_time = datetime.strptime('2017-02-01 00:00:00','%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime('2017-03-01 00:00:00','%Y-%m-%d %H:%M:%S')
        legal_name = store.manager
        while end_time <now_data:
            print "***",start_time
            print "---",end_time
            sql = "select fulfillment,product_sales, other,shipping_credits," \
                  "gift_wrap_credits,promotional_rebates,selling_fees,fba_fees,other_transaction_fees " \
                  "from statement_view " \
                  "where serial_number = '%s' and date_time>= '%s' and date_time<'%s' and type='%s'" %(serial_number,str(start_time),str(end_time),'Order');
            cur.execute(sql)
            product_sales = 0.0
            FBA_product_sales=0.0
            shipping_credits = 0.0
            gift_wrap_credits = 0.0
            promotional_rebates=0.0
            seller_fulfilled_selling_fees = 0.0
            FBA_selling_fees = 0.0
            fba_transaction_fees = 0.0
            other_transaction_fees = 0.0
            print sql
            for row in cur.fetchall():
                fulfillment_field = row[0]
                product_sales_field = row[1]
                other_field = row[2]
                shipping_credits_field = row[3]
                gift_wrap_credits_field = row[4]
                promotional_rebates_field = row[5]
                selling_fees_field = row[6]
                fba_fees_field = row[7]
                other_transaction_fees_field = row[8]
                ###product_sales---------------------
                try:
                    float1 = float(product_sales_field)
                except:
                    float1 = 0.0
                try:
                    float2 = float(other_field)
                except:
                    float2 = 0.0
                if fulfillment_field == "Seller":
                    product_sales += float1+float2
                elif fulfillment_field == "Amazon":
                    FBA_product_sales += float1+float2

                ##shipping_credits_field-----------
                try:
                    float3 = float(shipping_credits_field)
                except:
                    float3 = 0.0
                shipping_credits +=float3


                ##gift_wrap_credits------------------
                try:
                    float4 = float(gift_wrap_credits_field)
                except:
                    float4 = 0.0
                gift_wrap_credits +=float4

                ##promotional_rebates---------------
                try:
                    float5 = float(promotional_rebates_field)
                except:
                    float5 = 0.0
                promotional_rebates +=float5


                ##seller_fulfilled_selling_fees------
                try:
                    float6 = float(selling_fees_field)
                except:
                    float6 = 0.0
                if fulfillment_field == "Seller":
                    seller_fulfilled_selling_fees +=float6
                elif fulfillment_field == "Amazon":
                    FBA_selling_fees += float6

                ##fba_transaction_fee------
                # if fulfillment_field == "Amazon":
                try:
                    float7 = float(fba_fees_field)
                except:
                    float7 = 0.0
                fba_transaction_fees += float7


                ##other_transaction_fees
                try:
                    float8 = float(other_transaction_fees_field)
                except:
                    float8 = 0.0
                other_transaction_fees +=float8
            sql2 = "select fulfillment,product_sales, other,shipping_credits," \
                  "gift_wrap_credits,promotional_rebates,selling_fees,fba_fees,other_transaction_fees " \
                  "from statement_view " \
                  "where serial_number = '%s' and date_time>= '%s' and date_time<'%s' and type='%s'" %(serial_number,str(start_time),str(end_time),'Refund');
            cur.execute(sql2)
            product_refund = 0.0
            FBA_product_refund=0.0
            shipping_credits_refund = 0.0
            gift_wrap_credits_refund = 0.0
            promotional_rebates_refund = 0.0
            selling_fee_refund =0.0
            fba_transaction_fee_refunds =0.0
            other_transaction_fee_refunds =0.0
            for row in cur.fetchall():
                fulfillment_field = row[0]
                product_sales_field = row[1]
                other_field = row[2]
                shipping_credits_field = row[3]
                gift_wrap_credits_field = row[4]
                promotional_rebates_field = row[5]
                selling_fees_field = row[6]
                fba_fees_field = row[7]
                other_transaction_fees_field = row[8]

                ###product_refund---------------------
                try:
                    float1 = float(product_sales_field)
                except:
                    float1 = 0.0
                try:
                    float2 = float(other_field)
                except:
                    float2 = 0.0
                if fulfillment_field == "Seller":
                    product_refund += float1 + float2
                elif fulfillment_field == "Amazon":
                    FBA_product_refund += float1 + float2

                ##shipping_credits_refund-----------
                try:
                    float3 = float(shipping_credits_field)
                except:
                    float3 = 0.0
                shipping_credits_refund += float3

                ##gift_wrap_credits_refund------------------
                try:
                    float4 = float(gift_wrap_credits_field)
                except:
                    float4 = 0.0
                gift_wrap_credits_refund += float4

                ##promotional_rebates_refund---------------
                try:
                    float5 = float(promotional_rebates_field)
                except:
                    float5 = 0.0
                promotional_rebates_refund += float5

                ##selling_fee_refund------
                try:
                    float6 = float(selling_fees_field)
                except:
                    float6 = 0.0
                selling_fee_refund += float6

                ##fba_transaction_fee_refunds------
                if fulfillment_field == "Amazon":
                    try:
                        float7 = float(fba_fees_field)
                    except:
                        float7 = 0.0
                    fba_transaction_fee_refunds += float7

                ##other_transaction_fee_refunds
                try:
                    float8 = float(other_transaction_fees_field)
                except:
                    float8 = 0.0
                other_transaction_fee_refunds += float8

            sql3 = "select total,type,description  " \
                   "from statement_view " \
                   "where serial_number = '%s' and  date_time>= '%s' and date_time<'%s' and type not in ('%s','%s')" \
                   % (serial_number,str(start_time), str(end_time),"Refund", "Order");
            print "sql3:\t",sql3
            cur.execute(sql3)
            FBA_invenbry_credit = 0.0
            chargebacks = 0.0
            FBA_inventory_inbound_services_fees = 0.0
            Service_fees = 0.0
            cost_of_advertising = 0.0
            a_to_z_guarantee_chaims = 0.0
            Charges_to_credit_card = 0.0
            transfers_to_bank_account_sum = 0.0
            for row in cur.fetchall():
                total_filed = row[0]
                type_filed = row[1]
                description = row[2]
                try:
                    float1 = float(total_filed)
                except:
                    float1 = 0.0
                if type_filed == "FBA Inventory Fee" or type_filed == "FBA Customer Return Fee":
                    FBA_inventory_inbound_services_fees += float1
                if type_filed == "Service Fee":
                    if description == "Subscription Fee":
                        Service_fees += float1
                    elif description == "Cost of Advertising":
                        cost_of_advertising += float1
                if type_filed == "A-to-z Guarantee Glaim":
                    a_to_z_guarantee_chaims += float1
                if type_filed == "Chargebacks":
                    chargebacks += float1
                if type_filed == "Adjustment":
                    FBA_invenbry_credit +=float1
                if type_filed == "Dbt":
                    Charges_to_credit_card += float1
                if type_filed == "Transfer":
                    transfers_to_bank_account_sum +=float1

            expense_subtotal_debits = seller_fulfilled_selling_fees+FBA_selling_fees+fba_transaction_fees+other_transaction_fees+\
                                      FBA_inventory_inbound_services_fees+Shipping_label_purchases+Service_fees+\
                                      Refund_administration_fees+cost_of_advertising
            expense_subtotal_credits = selling_fee_refund+fba_transaction_fee_refunds+other_transaction_fee_refunds+Shipping_label_refunds+\
                                       carrier_shipping_label_adjustments+Adjustments+refund_for_advertiser
            summaries_expenses = Expenses = expense_subtotal_credits+expense_subtotal_debits
            income_subtotal_debits = product_refund+FBA_product_refund+shipping_credits_refund+gift_wrap_credits_refund+\
                                     promotional_rebates+a_to_z_guarantee_chaims+chargebacks
            income_subtotal_credits = product_sales+FBA_product_sales+FBA_invenbry_credit+shipping_credits+gift_wrap_credits+\
                                      promotional_rebates_refund
            summaries_income = Income = income_subtotal_debits+income_subtotal_credits

            summaries_transfers =  Transfers= Charges_to_credit_card+transfers_to_bank_account_sum

            subtotal_transfers = Charges_to_credit_card+Failed_transfers_to_bank_account

            year = start_time.year
            month = start_time.month
            params = {"serial_number":serial_number,"product_sales":product_sales,"product_refund":product_refund,
            "legal_name": legal_name,
            "FBA_product_sales":FBA_product_sales, "FBA_product_refund":FBA_product_refund,
            "FBA_invenbry_credit":FBA_invenbry_credit,"shipping_credits":shipping_credits,
            "shipping_credits_refund":shipping_credits_refund, "gift_wrap_credits":gift_wrap_credits,
            "gift_wrap_credits_refund":gift_wrap_credits_refund,"promotional_rebates":promotional_rebates,
            "promotional_rebates_refund":promotional_rebates_refund,"a_to_z_guarantee_chaims":a_to_z_guarantee_chaims,
            "chargebacks":chargebacks,"income_subtotal_debits":income_subtotal_debits,
            "income_subtotal_credits":income_subtotal_credits, "seller_fulfilled_selling_fees":seller_fulfilled_selling_fees,
            "FBA_selling_fees":FBA_selling_fees,"selling_fee_refund":selling_fee_refund,
            "fba_transaction_fee_refunds":fba_transaction_fee_refunds, "fba_transaction_fees":fba_transaction_fees,
            "FBA_inventory_inbound_services_fees":FBA_inventory_inbound_services_fees, "Shipping_label_purchases":Shipping_label_purchases,
            "Shipping_label_refunds":Shipping_label_refunds, "carrier_shipping_label_adjustments":carrier_shipping_label_adjustments,
            "Service_fees":Service_fees,"Adjustments":Adjustments, "Refund_administration_fees":Refund_administration_fees,
            "cost_of_advertising":cost_of_advertising, "refund_for_advertiser":refund_for_advertiser,
            "expense_subtotal_debits":expense_subtotal_debits, "expense_subtotal_credits":expense_subtotal_credits,
            "Income":Income, "Expenses":Expenses, "Charges_to_credit_card": Charges_to_credit_card,
            "transfers_to_bank_account_sum": transfers_to_bank_account_sum, "Failed_transfers_to_bank_account":Failed_transfers_to_bank_account,
            "summaries_income": summaries_income, "summaries_expenses": summaries_expenses,
            "Transfers":Transfers, "summaries_transfers": summaries_transfers,"subtotal_transfers":subtotal_transfers,
            "year": year, "month":month}
            svm = StatementViewMonth(**params)
            svm.save()
            start_time = add_months(start_time,1)
            end_time = add_months(end_time,1)



        break

def add_months(srcDate, addMonths):
    if not srcDate or not srcDate:        return None
    if addMonths < 1:        return srcDate
    month = srcDate.month - 1 + addMonths
    year = srcDate.year + month / 12
    month = month % 12 + 1
    day = min(srcDate.day, calendar.monthrange(year, month)[1])
    return srcDate.replace(year=year, month=month, day=day)


if __name__ =="__main__":
    handle_data()
