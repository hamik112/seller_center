#coding:utf-8
# Created bycc on 17-1-3.

import os
import datetime

from Amazon_api import Amazon_MWS



class Stores():
    def __init__(self,access_key,secret_key,store_key,store_token,region):
        self.access_key =access_key
        self.secret_key = secret_key
        self.store_key = store_key
        self.store_token = store_token
        self.region = region
def main():
    AMAZON_MWS = Amazon_MWS()
    access_key = 'AKIAI4QSPO5ISDC2GJYQ'
    secret_key = '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'
    store_key = 'A2TFDJE5MM2YVC'
    store_token = 'amzn.mws.2ea9e504-eb46-815c-bbe6-c19ea0ff9192'
    region = 'US'  #美国市场
    store_obj = Stores(access_key=access_key, secret_key=secret_key, store_key=store_key, store_token=store_token,
                       region=region)
    type = '_GET_AFN_INVENTORY_DATA_'
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H')
    fileName = str(now) +  '-FBA.txt'
    if not os.path.exists(fileName):
        os.system("touch %s"%fileName)
    # fileName = 'FBA.txt'
    result = AMAZON_MWS.get_product_report(store_obj,type=type,fileName=fileName)
    print result

if __name__ == "__main__":
    main();
