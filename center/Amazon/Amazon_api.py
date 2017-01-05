# -*- coding: utf-8 -*-



import HTMLParser
import Queue
import sys
import threading
import time
from xml.dom.minidom import  parseString

from config import CONFIG_MWS, CONFIG_MPI
from mws import Orders, Products, Inventory, Reports, Feeds, InboundShipments, Subscriptions, \
    MWSError

reload(sys)
sys.setdefaultencoding('utf8')

class Work(threading.Thread):
    def __init__(self, work_queue, result_queue, flag , lock, condition):
        threading.Thread.__init__(self)
        self._flag = {"flag" : True}
        self._lock = lock
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.wait = True
        self._condition = condition

    def run(self):
        #Dead cycle, to create threads under certain conditions close to exit
        while self._flag["flag"]:
            self._lock.acquire()
            if  self.work_queue.qsize() > 0:
                do = None
                args = None
                do, args = self.work_queue.get()#The task asynchronous dequeue, Queue internal implementation of the synchronization mechanism
                self._lock.release()
                try:
                    temp_result = do(args)
                    self.result_queue.put(temp_result)
                except Exception, e:
                    print "Unkown Exception", e
                    print str(do), str(args)
                    self.result_queue.put(None)
            else:
                self._lock.release()
                self._condition.acquire()
                self._condition.wait()
                self._condition.release()


class PoolManager(object):
    
    def __init__(self,threads=2):
        self.threads = []    
        self._flag = {"flag" : True}
        self.work_queue = Queue.Queue()
        self.work_num = 0
        self.result_queue = Queue.Queue()
        self._threadLock = threading.Lock()
        self._condition = threading.Condition()
        self.threads = threads
        self.__init_thread_pool(self.threads)
        
    def __init_thread_pool(self,threads):
        '''
        Initialization thread function 
        '''
        self.threads = []
        for i in range(threads):
            tempthreand = Work(self.work_queue, self.result_queue, self._flag, self._threadLock, self._condition)
            self.threads.append(tempthreand)
            tempthreand.start()

    def addJob(self, func, args):
        for arg in args:
            self.work_queue.put((func, arg))
            self.work_num = self.work_num + 1
        
        self.notify_all()


    def map(self, func, args):
        """
        Add a working team
        """
        for arg in args:
            self.work_queue.put((func, arg))#task enqueue, Queue internal synchronization mechanism
            self.work_num = self.work_num + 1
        
        self.notify_all()
                
        self.wait_jobscomplete()

        return self.getResult()

    def close(self):
        for t in self.threads:
            t._flag["flag"] = False
        
        self.notify_all()
    
        self.threads = []
    
    def getResult(self):
        result = []
        while self.result_queue.qsize() > 0:
            temp = self.result_queue.get()
            self.work_num = self.work_num - 1
            result.append(temp)
        return result
    
    def wait_jobscomplete(self):
        while 1:
            if self.work_num == self.result_queue.qsize():
                return 1

    def notify_all(self):
        self._condition.acquire()
        self._condition.notify_all()
        self._condition.release()

    def wait_allcomplete(self):
        """
        Wait for all threads to finish
        """   
        for item in self.threads:
            if item.isAlive():
                item.join()

    def activateFlag(self):
        '''
        all work are added into queue,
        After threads have finished all work, the threads will stop
        '''
        self._flag["flag"] = True


class create_api_exception(Exception):
    def __init__(self, value , locale):
         self.value = 'AWS.InvalidLocaleValue: ' + locale +' is not a valid value for Locale'
    def __str__(self):
       return repr(self.value)


class Amazon_MWS(object):
    '''
    amazon Merchant 相关,主要涉及到   网店订单获取,网店商品获取,网店商品库存获取,网店商品上传价格,
    '''
    def __create_api(self,type,account_info):
        
        access_key = account_info.access_key
        secret_key = account_info.secret_key
        account_id = account_info.store_key
        mws_auth_token = account_info.store_token
        region = account_info.region.upper()
            
        cfg = CONFIG_MWS[region]
        
        if type == 'Orders':
            return Orders(access_key, secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Inventory':
            return Inventory(access_key,secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Products':
            return Products(access_key,secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Reports':
            return Reports(access_key,secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Feeds':
            return Feeds(access_key,secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Inbounds':
            return InboundShipments(access_key,secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Subscriptions':
            return Subscriptions(access_key,secret_key, account_id,mws_auth_token,region = region)        
        else:
            error_msg = "Incorrect type supplied ('%(type)s')" % {"type" : type }
            raise MWSError(error_msg)
    
    def __get_inventory_list(self,Inventory_list):
        
        members_return_list = []
        for member_data in Inventory_list:
            members_data_list ={}
            members_data_list['TotalSupplyQuantity'] = get_element_by_tag(member_data,'TotalSupplyQuantity')
            members_data_list['SellerSKU'] = get_element_by_tag(member_data,'SellerSKU')
            members_data_list['ASIN'] = get_element_by_tag(member_data,'ASIN')
            members_data_list['FNSKU'] = get_element_by_tag(member_data,'FNSKU')
            members_data_list['Condition'] = get_element_by_tag(member_data,'Condition')
            members_data_list['InStockSupplyQuantity'] = get_element_by_tag(member_data,'InStockSupplyQuantity')
            members_return_list.append(members_data_list)
        return members_return_list
        
    def __get_order_line_list(self,order_items):
        html_parser = HTMLParser.HTMLParser()
        order_line_list = []
        for each_item in order_items:
            order_line_item = {}
            order_line_item['QuantityOrdered'] = get_element_by_tag(each_item,'QuantityOrdered')
            order_line_item['Title'] = get_element_by_tag(each_item,'Title')
            order_line_item['OrderItemId'] = get_element_by_tag(each_item,'OrderItemId')
            order_line_item['CurrencyCode'] = get_element_by_tag(each_item,'CurrencyCode')
            order_line_item['ItemPrice'] = get_element_by_tag(each_item,'ItemPrice','Amount')
            order_line_item['ItemTax'] = get_element_by_tag(each_item,'ItemTax','Amount')
            order_line_item['OrderItemId'] = get_element_by_tag(each_item,'OrderItemId')        
            order_line_item['ShippingPrice'] = get_element_by_tag(each_item,'ShippingPrice','Amount')
            order_line_item['ASIN'] = html_parser.unescape(html_parser.unescape(get_element_by_tag(each_item,'ASIN')))
            order_line_item['SellerSKU'] = html_parser.unescape(html_parser.unescape(get_element_by_tag(each_item,'SellerSKU')))
    #        order_line_item['image_url'] = get_amazon_img_url(product_amazon,MKPLACEID,IdType,[ASIN])
            order_line_list.append(order_line_item)
        return   order_line_list
    
    def __deal_amazon_data(self,orders,amazon):
        return_order_list = []
        for item in orders:
            return_order = {}
            return_order['orderID'] = get_element_by_tag(item,'AmazonOrderId')
    #        print 'order_id',return_order['orderID']
            return_order['order_Status'] = get_element_by_tag(item,'OrderStatus')
            return_order['total_Amount'] = get_element_by_tag(item,'OrderTotal','Amount')
            return_order['CurrencyCode'] = get_element_by_tag(item,'OrderTotal','CurrencyCode')
            return_order['ShipServiceLevel'] = get_element_by_tag(item,'ShipServiceLevel')
            return_order['Phone'] = get_element_by_tag(item,'ShippingAddress','Phone')
            return_order['PostalCode'] = get_element_by_tag(item,'ShippingAddress','PostalCode')
            return_order['Name'] = get_element_by_tag(item,'ShippingAddress','Name')
            return_order['CountryCode'] = get_element_by_tag(item,'ShippingAddress','CountryCode')
            return_order['StateOrRegion'] = get_element_by_tag(item,'ShippingAddress','StateOrRegion')
            return_order['AddressLine1'] = get_element_by_tag(item,'ShippingAddress','AddressLine1')
            return_order['AddressLine2'] = get_element_by_tag(item,'ShippingAddress','AddressLine2')
            return_order['AddressLine3'] = get_element_by_tag(item,'ShippingAddress','AddressLine3')
            return_order['City'] = get_element_by_tag(item,'ShippingAddress','City')
            return_order['BuyerEmail'] = get_element_by_tag(item,'BuyerEmail')
            return_order['BuyerName'] = get_element_by_tag(item,'BuyerName')
            return_order['PaymentMethod'] = get_element_by_tag(item,'PaymentMethod')
            return_order['PurchaseDate'] = get_element_by_tag(item,'PurchaseDate')
    
            order_items_obj = amazon.list_order_items(return_order['orderID'])
            data_2 = order_items_obj.response.content
            dom_2 = parseString(data_2)
            next_token_item = dom_2.getElementsByTagName("NextToken")
            order_items = dom_2.getElementsByTagName("OrderItem")
            order_line_list = []
            
            order_line_list.extend(self.__get_order_line_list(order_items))
    
            while len(next_token_item) != 0:
                order_items_obj_next = amazon.list_order_items_by_next_token(next_token_item[0].childNodes[0].data)
                next_data_2 = order_items_obj_next.response.content
                next_dom_2 = parseString(next_data_2)
                next_token_item = next_dom_2.getElementsByTagName("NextToken")
                next_order_items = next_dom_2.getElementsByTagName("OrderItem")
                
                order_line_list.extend(self.__get_order_line_list(next_order_items))
                
            return_order['OrderItem'] = order_line_list
            return_order_list.append(return_order)
        return return_order_list
    
    def __get_order(self,account_info,amazon_order_id):
        
        amazon = self.__create_api('Orders',account_info)
        order = amazon.get_order(amazon_order_id)
        order = order.response.content

    def __deal_product_price(self,price_items):
        price_list = []
        for each_item in price_items:
            order_price_item = {}
            if get_element_by_tag(each_item,'Error','Code') is not '':
                order_price_item['Type'] = get_element_by_tag(each_item,'Error','Type')
                order_price_item['Code'] = get_element_by_tag(each_item,'Error','Code')
                order_price_item['Message'] = get_element_by_tag(each_item,'Error','Message')
            else:
                order_price_item['ASIN'] = get_element_by_tag(each_item,'MarketplaceASIN','ASIN')
                order_price_item['SellerSKU'] = get_element_by_tag(each_item,'SKUIdentifier','SellerSKU')
                order_price_item['SellerId'] = get_element_by_tag(each_item,'SKUIdentifier','SellerId')
                order_price_item['LowestOfferListings'] =[]
                my_price_list = each_item.getElementsByTagName("LowestOfferListing")
                for each_price in my_price_list:
                    LowestOffer = {}
                    LowestOffer['ItemCondition'] = get_element_by_tag(each_price,'Qualifiers','ItemCondition')        
                    LowestOffer['ItemSubcondition'] = get_element_by_tag(each_price,'Qualifiers','ItemSubcondition')
                    LowestOffer['FulfillmentChannel'] = get_element_by_tag(each_price,'Qualifiers','FulfillmentChannel')
                    LowestOffer['ShipsDomestically'] = get_element_by_tag(each_price,'Qualifiers','ShipsDomestically')
                    LowestOffer['ShippingTime'] = get_element_by_tag(each_price,'ShippingTime','Max')        
                    LowestOffer['SellerPositiveFeedbackRating'] = get_element_by_tag(each_price,'Qualifiers','SellerPositiveFeedbackRating')
                    
                    LowestOffer['LandedPrice_Amount'] = get_element_by_tag(each_price,'LandedPrice','Amount')        
                    LowestOffer['LandedPrice_CurrencyCode'] = get_element_by_tag(each_price,'LandedPrice','CurrencyCode')
                    LowestOffer['ListingPrice'] = get_element_by_tag(each_price,'ListingPrice','Amount')
                    LowestOffer['ListingPrice_CurrencyCode'] = get_element_by_tag(each_price,'ListingPrice','CurrencyCode')        
                    LowestOffer['Shipping'] = get_element_by_tag(each_price,'Shipping','Amount')
                    LowestOffer['Shipping_CurrencyCode'] = get_element_by_tag(each_price,'Shipping','CurrencyCode')
                    
                    LowestOffer['SellerFeedbackCount'] = get_element_by_tag(each_price,'SellerFeedbackCount')
                    LowestOffer['NumberOfOfferListingsConsidered'] = get_element_by_tag(each_price,'NumberOfOfferListingsConsidered')
                    
                    order_price_item['LowestOfferListings'].append(LowestOffer)
            price_list.append(order_price_item)
        return   price_list
  
    def __deal_product_competitive_price(self,price_items):
        price_list = []
        for each_item in price_items:
            order_price_item = {}
            if get_element_by_tag(each_item,'Error','Code') is not '':
                order_price_item['Type'] = get_element_by_tag(each_item,'Error','Type')
                order_price_item['Code'] = get_element_by_tag(each_item,'Error','Code')
                order_price_item['Message'] = get_element_by_tag(each_item,'Error','Message')
            else:
                order_price_item['ASIN'] = get_element_by_tag(each_item,'MarketplaceASIN','ASIN')
                order_price_item['SellerSKU'] = get_element_by_tag(each_item,'SKUIdentifier','SellerSKU')
                order_price_item['SellerId'] = get_element_by_tag(each_item,'SKUIdentifier','SellerId')
                order_price_item['CompetitivePricing'] =[]
                my_price_list = each_item.getElementsByTagName("CompetitivePrice")
                for each_price in my_price_list:
                    CompetitiveOffer = {}
                    
                    CompetitiveOffer['CompetitivePriceId'] = get_element_by_tag(each_price,'CompetitivePriceId')
                    CompetitiveOffer['condition'] = str(each_price.getAttribute('condition'))
                    CompetitiveOffer['subcondition'] =str(each_price.getAttribute('subcondition'))
                    CompetitiveOffer['belongsToRequester'] = str(each_price.getAttribute('belongsToRequester'))
                    
                    CompetitiveOffer['LandedPrice_Amount'] = get_element_by_tag(each_price,'LandedPrice','Amount')        
                    CompetitiveOffer['LandedPrice_CurrencyCode'] = get_element_by_tag(each_price,'LandedPrice','CurrencyCode')
                    CompetitiveOffer['ListingPrice'] = get_element_by_tag(each_price,'ListingPrice','Amount')
                    CompetitiveOffer['ListingPrice_CurrencyCode'] = get_element_by_tag(each_price,'ListingPrice','CurrencyCode')        
                    CompetitiveOffer['Shipping'] = get_element_by_tag(each_price,'Shipping','Amount')
                    CompetitiveOffer['Shipping_CurrencyCode'] = get_element_by_tag(each_price,'Shipping','CurrencyCode')
                    
                    
                    order_price_item['CompetitivePricing'].append(CompetitiveOffer)
            price_list.append(order_price_item)
        return   price_list
     
    def get_product_price(self,account_info,SellerSKU=(),ASIN=(),condition=None,excludeme="False"):
        '''
        得到商店产品价格信息
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @param SellerSKU: 需要查找价格的SKU列表,最大值：20 个 SellerSKU
        @param ASIN: 需要查找的ASIN列表,最大值：20 个 ASIN
        @param condition: 根据商品状况筛纳入考虑范围的商品。有效值：New、Used、Collectible、Refurbished、Club
        @return: 返回此商店的产品价格列表，
                            格式为： 
                            
            
        '''
        try:

            amazon = self.__create_api('Products',account_info)
            
            marketplaceids = CONFIG_MPI[account_info.region]
            product_price_return_list = []
            
            
            if SellerSKU is not None:
                sku_list_count = 1
                while True:
                    SellerSKU_temp = SellerSKU[(sku_list_count-1)*20:sku_list_count*20]
                    sku_list_count += 1
                    if len(SellerSKU_temp) == 0:
                        break
                    else:
                        my_price_list = amazon.get_lowest_offer_listings_for_sku(marketplaceids, skus=SellerSKU_temp,condition=condition,excludeme=excludeme)
                        my_price_list = my_price_list.response.content
                        my_price_list = parseString(my_price_list)
                        my_price_list = my_price_list.getElementsByTagName("GetLowestOfferListingsForSKUResult")
                        product_price_return_list.extend(self.__deal_product_price(my_price_list))
                        
            elif ASIN is not None:
                asin_count = 1
                while True:
                    ASIN_temp = ASIN[(asin_count-1)*20:asin_count*20]
                    asin_count += 1
                    if len(ASIN_temp) == 0:
                        break
                    else:
                        my_price_list = amazon.get_lowest_offer_listings_for_asin(marketplaceids, asins=ASIN_temp,condition=condition,excludeme=excludeme)
                        my_price_list = my_price_list.response.content
                        my_price_list = parseString(my_price_list)
                        my_price_list = my_price_list.getElementsByTagName("GetLowestOfferListingsForASINResult")
                        product_price_return_list.extend(self.__deal_product_price(my_price_list))
            else:
                {'result': False, 'error_message': "SellerSKU and ASIN is can't be empty."}
            
            return {'result':True,'data':product_price_return_list}
        except Exception, e:
            return {'result':False,'error_message':str(e)}
    
    def get_product_competitive_price(self,account_info,SellerSKU=(),ASIN=()):
        '''
        得到商店产品价格信息
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @param SellerSKU: 需要查找价格的SKU列表,最大值：20 个 SellerSKU
        @param ASIN: 需要查找的ASIN列表,最大值：20 个 ASIN
        @return: 返回此商店的buybox价格，
                            格式为： 
                            [
                                {
                    'ASIN': 'B003RZ2F08',
                    'SellerId': 'ARWTKM5K67VQV',
                    'SellerSKU': '0B-K5PK-4COJ',
                    'CompetitivePricing':[{
                            'subcondition': u'New', 'condition': u'New','belongsToRequester': 'false',
                            'CompetitivePriceId': '1', 
                            'Shipping_CurrencyCode': 'USD','Shipping': '0.00', 
                            'LandedPrice_Amount': '3.10', 'ListingPrice_CurrencyCode': 'USD', 
                            'LandedPrice_CurrencyCode': 'USD', 'ListingPrice': '3.10', 
                                                     }]
                                }
                            ]
            
        '''
        try:
            amazon = self.__create_api('Products',account_info)
            
            marketplaceids = CONFIG_MPI[account_info.region]
            product_price_return_list = []
            
            
            if SellerSKU:
                sku_list_count = 1
                while True:
                    SellerSKU_temp = SellerSKU[(sku_list_count-1)*20:sku_list_count*20]
                    sku_list_count += 1
                    if len(SellerSKU_temp) == 0:
                        break
                    else:
                        my_price_list = amazon.get_competitive_pricing_for_sku(marketplaceids, skus=SellerSKU_temp)
                        my_price_list = my_price_list.response.content
                        my_price_list = parseString(my_price_list)
                        my_price_list = my_price_list.getElementsByTagName("GetCompetitivePricingForSKUResult")
                        product_price_return_list.extend(self.__deal_product_competitive_price(my_price_list))
                        
            elif ASIN:
                asin_count = 1
                while True:
                    ASIN_temp = ASIN[(asin_count-1)*20:asin_count*20]
                    asin_count += 1
                    if len(ASIN_temp) == 0:
                        break
                    else:
                        my_price_list = amazon.get_competitive_pricing_for_asin(marketplaceids, asins=ASIN_temp)
                        my_price_list = my_price_list.response.content
                        my_price_list = parseString(my_price_list)
                        my_price_list = my_price_list.getElementsByTagName("GetCompetitivePricingForASINResult")
                        product_price_return_list.extend(self.__deal_product_competitive_price(my_price_list))
            else:
                {'result': False, 'error_message': "SellerSKU and ASIN is can't be empty."}
            
            return {'result':True,'data':product_price_return_list}
        except Exception, e:
            return {'result':False,'error_message':str(e)}

    def get_reprot_test(self,account_info):
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report('_GET_FLAT_FILE_PAYMENT_SETTLEMENT_DATA_',)
            data = orders.response.content
            next_dom = parseString(data)

            FeedSubmissionId = get_element_by_tag(next_dom,'ReportRequestId')
            print 'FeedSubmissionId:',FeedSubmissionId
            while True:
                print 'start'
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                print 'data:',data
                next_dom = parseString(data)
                print 'status:',get_element_by_tag(next_dom,'ReportProcessingStatus')
                if get_element_by_tag(next_dom,'ReportProcessingStatus') == '_DONE_':
                    break
                print 'sleep(30)'
                time.sleep(30)

            FeedSubmissionId = get_element_by_tag(next_dom,'GeneratedReportId')
            orders = amazon.get_report(FeedSubmissionId)

            f = open('abc.txt','w')
            data = orders.response.content
            print '-------------华丽的分割线------------'
            print 'data',data
            f.write(data)
            f.flush()
            f.close()
            print '-------------华丽的分割线------------'
        except Exception,e:
            print 'error:',str(e)

    def get_product_report(self,account_info,type,fileName):
        '''
        获取店铺FBA库存信息API
        @param account_info: 店铺信息
        @param type:MWS的api获取报告的类型
        @param fileName:获取信息保存的文件路径
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report(type,)
            data = orders.response.content

            
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data
        
            while True:
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                next_dom = parseString(data)
                if next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data == '_DONE_':
                    break
                time.sleep(30)
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            orders = amazon.get_report(FeedSubmissionId)
            data = orders.response.content
            product_list_return = []
            product_list = data.split('\n')
            file_object = open(fileName, 'w')
            file_object.write(data)
            file_object.close()
#             print '----------------'
#             print product_list
#             print '----------------'
#             return
#             product_index = product_list[0].split('\t')
#             index_length = len(product_index)
#             start_index = 0
#
#             for each_product in product_list[1:]:
#                 product_temp = {}
#                 product_info  = each_product.split('\t')
#                 if len(product_info) <= 1:
#                     continue
#                 for i in range(0,index_length):
#                     product_temp[product_index[i]] = product_info[i]
#                 product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       
       
       
       
    def set_product_price(self,account_info,sku_price_list=()):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param sku_price_list: {sku1:{'price':price1,'currency':'USD','status':True},sku2:{'price':price2,'currency':'USD','status':True}}
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                            格式为： {
                        'data': {
                                    sku1:{'price':price1,'currency':'USD','status':True},
                                    sku1:{'price':price1,'currency':'USD','status':False,'ResultDescription':'Error description','ResultMessageCode':'00001'}
                                                     },
                         'result': True
                                         }
        '''
        try:
            amazon = self.__create_api('Feeds',account_info)
            MarketplaceID = CONFIG_MPI[account_info.region]
            messageId = 1
            my_feed = '''<?xml version="1.0" encoding="utf-8"?>
    <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
    <Header>
    <DocumentVersion>1.01</DocumentVersion>
    <MerchantIdentifier>%(Account_Id)s</MerchantIdentifier>
    </Header>
    <MessageType>Price</MessageType>'''
            
            my_feed = my_feed % { 'Account_Id': account_info.store_key }
            
            for each_sku in sku_price_list:
                SellerSku = each_sku
                SellPrice = sku_price_list[each_sku]['price']
                Currency = sku_price_list[each_sku]['currency']
                sku_price_list[each_sku]['status'] = True
                my_feed = my_feed + '''\n
    <Message>
        <MessageID>%(MessageID)s</MessageID>
        <OperationType>Update</OperationType>
        <Price>
        <SKU>%(MySku)s</SKU>
        <StandardPrice currency="%(currency)s">%(myprice)s</StandardPrice>
        </Price>
    </Message>'''
                my_feed = my_feed % {
                                     'MessageID':messageId,
                                      'MySku' : SellerSku,
                                      'myprice' : SellPrice,
                                      'currency':Currency
                                                        }
                messageId = messageId+1
            
            my_feed = my_feed + '''\n
</AmazonEnvelope>'''
#            print 'my_feed:',my_feed
            upload_result = amazon.submit_feed(my_feed, '_POST_PRODUCT_PRICING_DATA_')
            data = upload_result.response.content
            print 'data:',data
            print '--------------------------------'
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("FeedSubmissionId")[0].childNodes[0].data
#            FeedSubmissionId = '10799861466'
            while True:
                orders = amazon.get_feed_submission_list(feedids=[FeedSubmissionId])
                data = orders.response.content
                print 'data:',data
                print '--------------------------------'
                next_dom = parseString(data)
#                print '123'
                if next_dom.getElementsByTagName("FeedProcessingStatus")[0].childNodes[0].data == '_DONE_':
                    break
                time.sleep(5)
        
            sub_result_list = amazon.get_feed_submission_result(feedid = FeedSubmissionId)
            
            sub_result_list_xml = sub_result_list.response.content            
#            print 'data:',sub_result_list_xml
#            print '--------------------------------'
            sub_result_list_str = parseString(sub_result_list_xml)
            
#            print 'data:',sub_result_list_str
#            print '--------------------------------'
            
            
            MessagesProcessed = sub_result_list_str.getElementsByTagName("MessagesProcessed")[0].childNodes[0].data
            MessagesSuccessful = sub_result_list_str.getElementsByTagName("MessagesSuccessful")[0].childNodes[0].data
            
            if MessagesProcessed > MessagesSuccessful:
                for each in sub_result_list_str.getElementsByTagName("Result"):
                    sku_price_list[str(each.getElementsByTagName("MessageID")[0].childNodes[0].data)]['status'] = False
                    sku_price_list[str(each.getElementsByTagName("MessageID")[0].childNodes[0].data)]['ResultDescription'] = each.getElementsByTagName("ResultDescription")[0].childNodes[0].data
                    sku_price_list[str(each.getElementsByTagName("MessageID")[0].childNodes[0].data)]['ResultMessageCode'] = each.getElementsByTagName("ResultMessageCode")[0].childNodes[0].data
            
            return {'result':True,'data':sku_price_list}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
        
    def set_product_quantity(self,account_info,sku_inventory_list=()):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param sku_price_list: {sku1:{'Quantity':2,'status':True},sku2:{'Quantity':0,'status':True}}
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                            格式为： {
                        'data': {
                                   sku1:{'Quantity':2,status':True},
                                   sku1:{'Quantity':2,status':True,'ResultDescription':'Error description','ResultMessageCode':'00001'}
                                                     },
                         'result': True
                                         }
        '''
        try:
            amazon = self.__create_api('Feeds',account_info)
            MarketplaceID = CONFIG_MPI[account_info.region]
            messageId = 1
            my_feed = '''<?xml version="1.0" encoding="utf-8"?>
    <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
    <Header>
    <DocumentVersion>1.01</DocumentVersion>
    <MerchantIdentifier>%(Account_Id)s</MerchantIdentifier>
    </Header>
    <MessageType>Inventory</MessageType>'''
            
            my_feed = my_feed % { 'Account_Id': account_info.store_key }
            
            for each_sku in sku_inventory_list:
                SellerSku = each_sku
                SellerInventory= sku_inventory_list[each_sku]['Quantity']
                sku_inventory_list[each_sku]['status'] = True
                my_feed = my_feed + '''\n
    <Message>
        <MessageID>%(MessageID)s</MessageID>
        <OperationType>Update</OperationType>
          <Inventory>
                   <SKU>%(MySku)s</SKU>
                   <FulfillmentCenterID>DEFAULT</FulfillmentCenterID>
                   <Quantity>%(quantity)s</Quantity>
         </Inventory>
    </Message>'''
                my_feed = my_feed % {
                                     'MessageID':messageId,
                                      'MySku' : SellerSku,
                                      'quantity' : SellerInventory,
                                                        }
                messageId = messageId+1
            
            my_feed = my_feed + '''\n
</AmazonEnvelope>'''
            error_info = 'timed'
            while 'timed' in error_info:
                try:
                    upload_result = amazon.submit_feed(my_feed, '_POST_INVENTORY_AVAILABILITY_DATA_',[MarketplaceID])
                    error_info = ''
                except Exception,e:
                    print e
                    error_info =  str(e)
                    
                
            data = upload_result.response.content
            print 'data:',data
            print '--------------------------------'
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("FeedSubmissionId")[0].childNodes[0].data
#            FeedSubmissionId = '10799861466'
            _count = 0
            while True:
                if _count == 0:
                    time.sleep(120)
                    _count += 1
                else:
                    time.sleep(60)
                error_info = 'timed'
                while 'timed' in error_info:
                    try:
                        orders = amazon.get_feed_submission_list(feedids=[FeedSubmissionId])
                        error_info = ''
                    except Exception,e:
                        error_info =  str(e)
                
                data = orders.response.content
                print 'data:',data
                print '--------------------------------'
                next_dom = parseString(data)
#                print '123'
                if next_dom.getElementsByTagName("FeedProcessingStatus")[0].childNodes[0].data == '_DONE_':
                    break
                
            error_info = 'timed'
            while 'timed' in error_info:
                try:
                    sub_result_list = amazon.get_feed_submission_result(feedid = FeedSubmissionId)
                    error_info = ''
                except Exception,e:
                    error_info =  str(e)
            sub_result_list_xml = sub_result_list.response.content            
            sub_result_list_str = parseString(sub_result_list_xml)
            MessagesProcessed = sub_result_list_str.getElementsByTagName("MessagesProcessed")[0].childNodes[0].data
            MessagesSuccessful = sub_result_list_str.getElementsByTagName("MessagesSuccessful")[0].childNodes[0].data
            error_list = []
            if MessagesProcessed > MessagesSuccessful:
                for each in sub_result_list_str.getElementsByTagName("Result"):
                    error_list.append(each.getElementsByTagName("MessageID")[0].childNodes[0].data)
            print error_list
            error_skus = []
            error_list = [int(_id) for _id in set(error_list)]
            for _index in error_list:
                error_skus.append(sku_inventory_list.keys()[_index-1])
                sku_inventory_list.pop(sku_inventory_list.keys()[_index-1])
            return {'result':True,'data':sku_inventory_list,'error_skus':error_skus}
        except Exception,e:
            return {'result':False,'error_message':str(e)}

    
    def get_fba_product_inventory(self,account_info, sku_list=(),datetime = None ):
        '''
            得到网店的FBA商品的库存信息
        @param ACCOUMNT_ID: 商店标示
        @param regioin: 地区标示
        @param sku_list:需要查找的商品列表
        @param datetime: 商品库存信息发生变化的起始时间
        @return: 设置sku_list的话返回指定的列表
                              格式：{
                        'data': [
                                    {'ASIN': '', 'SellerSKU': 'B00475IIA8', 'FNSKU': '', 'InStockSupplyQuantity': '0', 'Condition': '', 'TotalSupplyQuantity': '0'},
                                                     ],
                         'result': True
                                         }
        '''

        amazon = self.__create_api('Inventory',account_info)
        fba_product_inventory_return_list = []
    
        floop_count = 1
        while True:
            sku_list_temp = sku_list[(floop_count-1)*50:floop_count*50]
            if len(sku_list_temp) == 0:
                break
            else:
                try:
                    orders = amazon.list_inventory_supply(skus=sku_list_temp,datetime=datetime)
                    next_data_2 = orders.response.content
                    next_dom_2 = parseString(next_data_2)
                    Inventory_list = next_dom_2.getElementsByTagName("member")
                    fba_product_inventory_return_list.extend(self.__get_inventory_list(Inventory_list))
                    floop_count = floop_count+1
                except Exception,e:
                    print 'error:',str(e)
            time.sleep(10)
        return {'result':True,'data':fba_product_inventory_return_list}
    
    
    
    
    def get_listing_report(self,account_info,repoprt_type,start_date= None,end_date=None):
        '''
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                 {'key1': 'value1', 'key2': 'value2', ...},
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report(repoprt_type)
            data = orders.response.content
       
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data

            while True:
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                next_dom = parseString(data)
                if next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data in ['_DONE_','_CANCELLED_','_DONE_NO_DATA_']:
                    break
                time.sleep(60)
                
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            orders = amazon.get_report(FeedSubmissionId)
            
            data = orders.response.content
            
            product_list_return = []
            product_list = data.replace('\r','').split('\n')

            product_index = product_list[0].split('\t')
            index_length = len(product_index)
            start_index = 0
            
            for each_product in product_list[1:]:
                product_temp = {}
                product_info  = each_product.split('\t')
                if len(product_info) <= 1:
                    continue
                for i in range(0,index_length):
                    product_temp[product_index[i]] = product_info[i]
                product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       

    
    

    def get_payment_report(self,account_info,start_date= None,end_date=None):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                {'SKU': '123456','title':'abc'}, {'SKU': '456789','title':'efg'}
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report('_GET_FLAT_FILE_ORDERS_DATA_',start_date,end_date)
            data = orders.response.content
        
            next_dom = parseString(data)
            print data
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data
            print FeedSubmissionId
#             return
#             FeedSubmissionId = '59897016421' 
            while True:
#                 print 'sleep 60s'
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                next_dom = parseString(data)
                print data
                print next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data
                if next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data == '_DONE_':
                    break
                time.sleep(60)
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            orders = amazon.get_report(FeedSubmissionId)
            
            data = orders.response.content
            print 'success!!!!!'
            print data
            
            product_list_return = []
            product_list = data.split('\n')
#             print '----------------'
#             print product_list
#             print '----------------'
#             return
            product_index = product_list[0].split('\t')
            index_length = len(product_index)
            start_index = 0
            
            for each_product in product_list[1:]:
                product_temp = {}
                product_info  = each_product.split('\t')
                if len(product_info) <= 1:
                    continue
                for i in range(0,index_length):
                    product_temp[product_index[i]] = product_info[i]
                product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       



    def get_fba_health_inventory_report(self,account_info):
        '''
        得到FBA 产品的产品库存销量信息，预计可销天数。
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                 {'inv-age-91-to-180-days': '77', 'weeks-of-cover-t180': '116.5', 'units-shipped-last-365-days': '17', 
                                 'inbound-recommend-quantity': '', 'lowest-afn-new-price': '12.24', 'lowest-afn-used-price': '0.00', 
                                 'asin-limit': '', 'inv-age-365-plus-days': '0', 'sellable-quantity': '77', 'inv-age-0-to-90-days': '0', 
                                 'currency': 'USD', 'qty-to-be-charged-long-term-storage-in-next-cleanup': '0', 'inv-age-181-to-270-days': '0',
                                  'per-unit-volume': '0.0', 'sku': 'Ash-B005MRAXZI', 'asin': 'B005MRAXZI', 'lowest-mfn-used-price': '0.00', 
                                  'lowest-mfn-new-price': '12.20    ', 'fnsku': 'X000KGFYNX', 'weeks-of-cover-t90': '82.5', 'sales-price': '12.24', 
                                  'sales-rank': '141361', 'units-shipped-last-90-days': '12', 'product-name': 'Dayan 5 ZhanChi 3x3x3 Speed Cube White DIY Kit', 
                                  'units-shipped-last-180-days': '17', 'is-hazmat': 'N', 'qty-in-long-term-storage-program': '0', 'inv-age-271-to-365-days': '0',
                                   'weeks-of-cover-t30': '330', 'snapshot-date': '2014-12-14T08:00:00+00:00', 'qty-with-removals-in-progress': '0', 
                                   'in-bound-quantity': '0', 'units-shipped-last-7-days': '1', 'your-price': '12.24', 'condition': 'New',
                                    'num-afn-used-sellers': '0', 'units-shipped-last-24-hrs': '0', 'unsellable-quantity': '0', 'weeks-of-cover-t365': '236.2',
                                     'units-shipped-last-30-days': '1', 'weeks-of-cover-t7': '77', 'projected-long-term-storage-fees': '0.00', 'total-quantity': '79',
                                      'num-afn-new-sellers': '2', 'product-group': 'toy_display_on_website'},
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report('_GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA_')
            data = orders.response.content
       
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data
            print FeedSubmissionId

            while True:
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                next_dom = parseString(data)
                print next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data
                if next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data in ['_DONE_','_CANCELLED_','_DONE_NO_DATA_']:
                    break
                time.sleep(60)
                
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            orders = amazon.get_report(FeedSubmissionId)
            
            data = orders.response.content
            
            product_list_return = []
            product_list = data.replace('\r','').split('\n')

            product_index = product_list[0].split('\t')
            index_length = len(product_index)
            start_index = 0
            
            for each_product in product_list[1:]:
                product_temp = {}
                product_info  = each_product.split('\t')
                if len(product_info) <= 1:
                    continue
                for i in range(0,index_length):
                    if product_info[i] == '':
                        product_temp[product_index[i]] = '0'
                    elif product_info[i] == 'Infinite':
                        product_temp[product_index[i]] = '9999'
                    else:
                        product_temp[product_index[i]] = product_info[i]
                        
                product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       



    def get_fba_listing_inventory_report(self,account_info):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                {'sku': '0E-4AS0-OGYA', 'asin': 'B008ATNE8I', 'afn-fulfillable-quantity': '22', 'your-price': '61.99', 'fnsku': 'X000O6JOHB', 'afn-total-quantity': '23', 'afn-listing-exists': 'Yes', 'afn-warehouse-quantity': '23', 'mfn-listing-exists': 'No', 'afn-unsellable-quantity': '0', 'mfn-fulfillable-quantity': '', 'afn-inbound-shipped-quantity': '0', 'afn-reserved-quantity': '1', 'product-name': 'Pixel Vertical Battery Grip for Canon EOS 5D Mark III BG-E11', 'per-unit-volume': '0.1', 'afn-inbound-receiving-quantity': '0', 'condition': 'New', 'afn-inbound-working-quantity': '0'}
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report('_GET_FBA_MYI_ALL_INVENTORY_DATA_')
            data = orders.response.content
     
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data
            while True:
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                next_dom = parseString(data)
                if '_DONE_' in next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data:
                    break
                time.sleep(60)
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            orders = amazon.get_report(FeedSubmissionId)
            
            data = orders.response.content

            
            product_list_return = []
            product_list = data.split('\n')

            product_index = product_list[0].split('\t')
            index_length = len(product_index)
            start_index = 0
            
            for each_product in product_list[1:]:
                product_temp = {}
                product_info  = each_product.split('\t')
                if len(product_info) <= 1:
                    continue
                for i in range(0,index_length):
                    product_temp[product_index[i]] = product_info[i]
                product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       


    def get_payment_settlement_reports(self,account_info):
        try:
            amazon = self.__create_api('Reports',account_info)
            settlements = amazon.get_report_request_list(types = ['_GET_ALT_FLAT_FILE_PAYMENT_SETTLEMENT_DATA_'])
            data = settlements.response.content
            next_dom = parseString(data)
            
            report_list_return = []
            report_lists = next_dom.getElementsByTagName("ReportRequestInfo")
            for each in report_lists:
                r = {
                     'request_id':each.getElementsByTagName("ReportRequestId")[0].childNodes[0].data,
                     'start_date':each.getElementsByTagName("StartDate")[0].childNodes[0].data,
                     'end_date':each.getElementsByTagName("EndDate")[0].childNodes[0].data,
                     'generated_id':each.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
                     }
                report_list_return.append(r)
            return {'result':True,'data':report_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
            
    def get_payment_settlement_detail(self,account_info,report_id):
        try:
            amazon = self.__create_api('Reports',account_info)
            settlements = amazon.get_report(report_id)
            data = settlements.response.content
   
            settlement_list_return = []
            settlement_list = data.split('\n')

            settlement_index = settlement_list[0].split('\t')
            index_length = len(settlement_index)
            start_index = 0
            
            for each_settlement in settlement_list[1:]:
                settlement_temp = {}
                settlement_info  = each_settlement.split('\t')
                if len(settlement_info) <= 1:
                    continue
                for i in range(0,index_length):
                    settlement_temp[settlement_index[i]] = settlement_info[i]
                settlement_list_return.append(settlement_temp)
                
            return {'result':True,'data':settlement_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
            



    def get_fba_inventory_receipts_data_report(self,account_info,start_date= None,end_date=None):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                 {'sku': 'NJ-15MP-OPVH', 'fnsku': 'X000P1X3G3', 'received-date': '2014-12-09T08:00:00+00:00', 'fulfillment-center-id': 'AVP1', 'product-name': 'ThinkMax\xae 4 In 1 X4 Battery Charger for Hubsan', 'fba-shipment-id': 'FBA28XS7QB', 'quantity': '200'},
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            inventories = amazon.request_report('_GET_FBA_FULFILLMENT_INVENTORY_RECEIPTS_DATA_',start_date,end_date)
            data = inventories.response.content
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data
            while True:
                inventories = amazon.get_report_request_list([FeedSubmissionId])
                data = inventories.response.content
                next_dom = parseString(data)
                if '_DONE_' in next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data:
                    break
                time.sleep(2 * 60)
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            product_inventories = amazon.get_report(FeedSubmissionId)
            
            data = product_inventories.response.content
            
            product_list_return = []
            product_list = data.split('\n')

            product_index = product_list[0].split('\t')
            index_length = len(product_index)
            start_index = 0
            
            for each_product in product_list[1:]:
                product_temp = {}
                product_info  = each_product.split('\t')
                if len(product_info) <= 1:
                    continue
                for i in range(0,index_length):
                    product_temp[product_index[i]] = product_info[i]
                product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       
       
    def get_shipment_data(self,ShipmentData):
        shipment_list = []
        try:
            for each_shipment in ShipmentData:
                r = {
                     'PostalCode' : each_shipment.getElementsByTagName("PostalCode")[0].childNodes[0].data,
                     'Name' : each_shipment.getElementsByTagName("Name")[0].childNodes[0].data,
                     'CountryCode' : each_shipment.getElementsByTagName("CountryCode")[0].childNodes[0].data,
                     'StateOrProvinceCode' : each_shipment.getElementsByTagName("StateOrProvinceCode")[0].childNodes[0].data,
                     'AddressLine2' : '',#each_shipment.getElementsByTagName("AddressLine2")[0].childNodes[0].data,                     
                     'AddressLine1' : each_shipment.getElementsByTagName("AddressLine1")[0].childNodes[0].data,
                     'City' : each_shipment.getElementsByTagName("City")[0].childNodes[0].data,
                     'AreCasesRequired' : each_shipment.getElementsByTagName("AreCasesRequired")[0].childNodes[0].data,
                     'ShipmentName' : each_shipment.getElementsByTagName("ShipmentName")[0].childNodes[0].data,
                     'ShipmentStatus' : each_shipment.getElementsByTagName("ShipmentStatus")[0].childNodes[0].data,
                     'ShipmentId' : each_shipment.getElementsByTagName("ShipmentId")[0].childNodes[0].data,
                     'LabelPrepType' : each_shipment.getElementsByTagName("LabelPrepType")[0].childNodes[0].data,
                     'DestinationFulfillmentCenterId' : each_shipment.getElementsByTagName("DestinationFulfillmentCenterId")[0].childNodes[0].data,
                     }
                shipment_list.append(r)
        except Exception,e:
            print 'get_shipment_data ',e
        return shipment_list


    def get_fba_inbound_data(self,account_info,start_date= None,end_date=None):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                 {'sku': 'NJ-15MP-OPVH', 'fnsku': 'X000P1X3G3', 'received-date': '2014-12-09T08:00:00+00:00', 'fulfillment-center-id': 'AVP1', 'product-name': 'ThinkMax\xae 4 In 1 X4 Battery Charger for Hubsan', 'fba-shipment-id': 'FBA28XS7QB', 'quantity': '200'},
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Inbounds',account_info)
            shipments = amazon.list_inbound_shipments(start_date,end_date)
            data = shipments.response.content
            print data
            next_dom = parseString(data)
            
            ShipmentData = next_dom.getElementsByTagName("member")
            
            shipment_list = self.get_shipment_data(ShipmentData)
            next_token_tag = next_dom.getElementsByTagName("NextToken")
            
            while next_token_tag:
                
                next_token = next_dom.getElementsByTagName("NextToken")[0].childNodes[0].data
                shipments = amazon.list_inbound_shipments_by_nexttoken(next_token)
                data = shipments.response.content
                next_dom = parseString(data)
    
                ShipmentData = next_dom.getElementsByTagName("member")
                shipment_list.extend(self.get_shipment_data(ShipmentData))
                next_token_tag = next_dom.getElementsByTagName("NextToken")
                
            return {'result':True,'data':shipment_list}
        except Exception,e:
            raise
            return {'result':False,'error_message':str(e)}
       

 
    def get_shipment_items_data(self,ShipmentData):
        shipment_list = []
        try:
            for each_shipment in ShipmentData:
                r = {
                     'SellerSKU' : each_shipment.getElementsByTagName("SellerSKU")[0].childNodes[0].data,
                     'QuantityShipped' : each_shipment.getElementsByTagName("QuantityShipped")[0].childNodes[0].data,
                     'QuantityInCase' : each_shipment.getElementsByTagName("QuantityInCase")[0].childNodes[0].data,
                     'QuantityReceived' : each_shipment.getElementsByTagName("QuantityReceived")[0].childNodes[0].data,
                     'FulfillmentNetworkSKU' : each_shipment.getElementsByTagName("FulfillmentNetworkSKU")[0].childNodes[0].data,
                     }
                shipment_list.append(r)
        except Exception,e:
            print 'get_shipment_items_data ',e
        return shipment_list




    def get_fba_inbound_shipment_items(self,account_info,shipment_id):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                 {'sku': 'NJ-15MP-OPVH', 'fnsku': 'X000P1X3G3', 'received-date': '2014-12-09T08:00:00+00:00', 'fulfillment-center-id': 'AVP1', 'product-name': 'ThinkMax\xae 4 In 1 X4 Battery Charger for Hubsan', 'fba-shipment-id': 'FBA28XS7QB', 'quantity': '200'},
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Inbounds',account_info)
            inventories = amazon.list_inbound_shipment_items(shipment_id)
            data = inventories.response.content
            next_dom = parseString(data)
            
            ShipmentData = next_dom.getElementsByTagName("member")
            shipment_list = self.get_shipment_items_data(ShipmentData)
            next_token_tag = next_dom.getElementsByTagName("NextToken")
            
            while next_token_tag:
                
                next_token = next_dom.getElementsByTagName("NextToken")[0].childNodes[0].data
                shipments = amazon.list_inbound_shipment_items_by_nexttoken(next_token)
                data = shipments.response.content
                next_dom = parseString(data)
    
                ShipmentData = next_dom.getElementsByTagName("member")
                shipment_list.extend(self.get_shipment_items_data(ShipmentData))
                next_token_tag = next_dom.getElementsByTagName("NextToken")
                            
                       
            return {'result':True,'data':shipment_list}
        except Exception,e:
            raise
            return {'result':False,'error_message':str(e)}
       
       
       
    def create_destination(self,account_info):
        amazon = self.__create_api('Subscriptions',account_info)
        destination = amazon.registerDestination('ATVPDKIKX0DER')
        data = destination.response.content
        print data
        return data
    
       
    def test_notification_to_destination(self,account_info):
        amazon = self.__create_api('Subscriptions',account_info)
        destination = amazon.testNotificationToDestination('ATVPDKIKX0DER')
        data = destination.response.content
        print data
        return data
    
    def get_list_registered_destinations(self,account_info):
        amazon = self.__create_api('Subscriptions',account_info)
        destination = amazon.getListRegisteredDestinations('ATVPDKIKX0DER')
        data = destination.response.content
        print data
        return data    
    
    
def get_element_by_tag(item,name1,name2=None):
    value = item.getElementsByTagName(name1)
    if len(value) ==0:
        value = ""
    elif name2 is None :
        try:
            value = value[0].childNodes[0].data
        except:
            value =""
    else:
        value = get_element_by_tag(value[0],name2)
    return value