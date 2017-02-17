# encoding:utf-8

from django.db.models import Q

from manageApp.models import StatementView




class StatementViewData(object):
    def __init__(self, serial_number):
        self.serial_number =  serial_number
        pass

    def orders_product_charges(self):
        query_select = Q(serial_number=self.serial_number)
        query_select = query_select & Q()
        
        pass

    def orders_promo_rebates(self):
        pass

    def orders_amazon_fees(self):
        pass

    def orders_other(self):

        pass

    
    
    def refunds_product_charges(self):
        pass

    def refunds_amazon_fees(self):
        pass

    def refunds_other(self):
        pass



    def selling_fees(self):
        pass
    def selling_cost_of_advertising(self):
        pass



    def other_transactions(self):
        pass

    
    def closing_banlance_total(self):
        pass

    def closing_banlance_unavailable(self):
        pass
    def closing_balance_view_details(self):
        pass


    def transfer_amount_initiated(self):
        pass

    




    
