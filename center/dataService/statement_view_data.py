#/usr/bin/env python
# encoding:utf8


from manageApp.models import StatementView


class StatementViewData(object):
    def __init__(self, post_dict):
        self.post_dict = post_dict
        pass



    def statement_data_read(self):
        if self.post_dict.get("reportType", "") == "Summary":    # 导出pdf

            pass
        elif self.post_dict.get("reportType", "") == "Transaction":   #导出表格

            pass
        statement_list = StatementView.objects.filter()
        return list(statement_list.values())


    def test_return(self):
        return {"unsuccessful_charges": "57",
                "seller_repayment": "37.7",
                "seller_repayment_subtotal": "37.7",
                "product_charges": "0.1",
                "promo_rebates": "0.2",
                "amazon_fees": "0.3",
                "other": "0.4",
                "other_subtotal": "0.5",
                "product_charges": "0.6",
                "product_charges_subtotal": "0.7"
                }



