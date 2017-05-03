# -*- coding: utf-8 -*-
import calendar
import sys

from manageApp.models import FilenameToStorename,StatementViewMonth

reload(sys)
sys.setdefaultencoding('utf-8')

def create_statement_month(serial_number,obj,statement_datas):
    stores  = FilenameToStorename.objects.filter(serial_number=serial_number).first()
    if not stores:
        return None
    Shipping_label_purchases = 0
    Shipping_label_refunds = 0
    carrier_shipping_label_adjustments = 0
    Adjustments = 0
    Refund_administration_fees = 0
    refund_for_advertiser = 0
    Failed_transfers_to_bank_account = 0
    serial_number = stores.serial_number
    legal_name = stores.manager
    product_sales = 0.0
    FBA_product_sales=0.0
    shipping_credits = 0.0
    gift_wrap_credits = 0.0
    promotional_rebates=0.0
    seller_fulfilled_selling_fees = 0.0
    FBA_selling_fees = 0.0
    fba_transaction_fees = 0.0
    other_transaction_fees = 0.0
    product_refund = 0.0
    FBA_product_refund = 0.0
    shipping_credits_refund = 0.0
    gift_wrap_credits_refund = 0.0
    promotional_rebates_refund = 0.0
    selling_fee_refund = 0.0
    fba_transaction_fee_refunds = 0.0
    other_transaction_fee_refunds = 0.0
    FBA_invenbry_credit = 0.0
    chargebacks = 0.0
    FBA_inventory_inbound_services_fees = 0.0
    Service_fees = 0.0
    cost_of_advertising = 0.0
    a_to_z_guarantee_chaims = 0.0
    Charges_to_credit_card = 0.0
    transfers_to_bank_account_sum = 0.0

    for year in obj:
        obj_month = obj.get(year)
        for month in obj_month:
            statement_datas = obj_month.get(month)
            for row in statement_datas:
                type = row.type
                fulfillment_field = row.fulfillment
                product_sales_field = row.product_sales
                other_field = row.other
                shipping_credits_field = row.shipping_credits
                gift_wrap_credits_field = row.gift_wrap_credits
                promotional_rebates_field = row.promotional_rebates
                selling_fees_field = row.selling_fees
                fba_fees_field = row.fba_fees
                other_transaction_fees_field = row.other_transaction_fees
                total_filed = row.total
                description = row.description
                try:
                    float1 = float(product_sales_field)
                except:
                    float1 = 0.0
                try:
                    float2 = float(other_field)
                except:
                    float2 = 0.0
                try:
                    float3 = float(shipping_credits_field)
                except:
                    float3 = 0.0
                try:
                    float4 = float(gift_wrap_credits_field)
                except:
                    float4 = 0.0
                try:
                    float5 = float(promotional_rebates_field)
                except:
                    float5 = 0.0
                try:
                    float6 = float(selling_fees_field)
                except:
                    float6 = 0.0
                try:
                    float7 = float(fba_fees_field)
                except:
                    float7 = 0.0
                try:
                    float8 = float(other_transaction_fees_field)
                except:
                    float8 = 0.0
                try:
                    float9 = float(total_filed)
                except:
                    float9 = 0.0
                if type == "Order":
                    if fulfillment_field == "Seller":
                        product_sales += float1 + float2
                        seller_fulfilled_selling_fees += float6
                    elif fulfillment_field == "Amazon":
                        FBA_product_sales += float1 + float2
                        FBA_selling_fees += float6
                    shipping_credits += float3
                    gift_wrap_credits += float4
                    promotional_rebates += float5
                    fba_transaction_fees += float7
                    other_transaction_fees += float8
                elif type == "Refund":
                    if fulfillment_field == "Seller":
                        product_refund += float1 + float2
                    elif fulfillment_field == "Amazon":
                        FBA_product_refund += float1 + float2
                    shipping_credits_refund += float3
                    gift_wrap_credits_refund += float4
                    promotional_rebates_refund += float5
                    selling_fee_refund += float6
                    fba_transaction_fee_refunds += float7
                    other_transaction_fee_refunds += float8
                elif type == "FBA Inventory Fee" or type == "FBA Customer Return Fee":
                    FBA_inventory_inbound_services_fees += float9
                elif type == "Service Fee":
                    if description == "Subscription Fee":
                        Service_fees += float9
                    elif description == "Cost of Advertising":
                        cost_of_advertising += float9
                elif type == "A-to-z Guarantee Glaim":
                    a_to_z_guarantee_chaims += float9
                elif type == "Chargebacks":
                    chargebacks += float9
                elif type == "Adjustment":
                    FBA_invenbry_credit += float9
                elif type == "Dbt":
                    Charges_to_credit_card += float9
                elif type == "Transfer":
                    transfers_to_bank_account_sum += float9

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
            svm = StatementViewMonth.objects.filter(year=year, month=month, serial_number=serial_number).first()
            if not svm:
                svm = StatementViewMonth(**params)
                svm.save()
            else:
                for key in svm.__dict__:
                    svm.__dict__[key] =str(float(svm.__dict__[key]) + float(params.get(key,'0')))
                svm.save()






def add_months(srcDate, addMonths):
    if not srcDate or not srcDate:        return None
    if addMonths < 1:        return srcDate
    month = srcDate.month - 1 + addMonths
    year = srcDate.year + month / 12
    month = month % 12 + 1
    day = min(srcDate.day, calendar.monthrange(year, month)[1])
    return srcDate.replace(year=year, month=month, day=day)


