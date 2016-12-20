#!/usr/bin/env python
# encoding:utf-8

from django.conf import  settings

from center.models import  AllStatements


class AllStatementsList(object):
    def __init__(self, username):
        self.username = username
        pass

    def get_all_statements_file(self):
        try:
            all_statements_list = AllStatements.objects.filter(username=self.username).values("settlement_period",
            "beginning_balance","product_charges_total", "promo_retates_total", "amazon_fees_total", "other_total",
            "deposit_total","filename")
        except Exception,e :
            all_statements_list = []
        return all_statements_list