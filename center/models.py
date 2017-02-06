# encoding:utf-8

from django.db import models
from django.contrib.auth.models import User

from django.utils import  timezone
# Create your models here.


class GenerateReport(models.Model):
    """ date range reports 请求记录 """
    id = models.AutoField(primary_key=True, null=False)
    is_custom        =  models.CharField( max_length= 30, default="", null=False)
    reportType       =  models.CharField( max_length= 30, default="", null=False)       #report 类型,
    year             =  models.CharField( max_length= 200, default="", null=False)                #
    timeRangeType     =  models.CharField(max_length= 100, default="", null=False)      #时间段
    month             =  models.CharField( max_length= 100, default="", null=False)     #月份
    timeRange         =  models.CharField( max_length=50, default="", null=False)
    report_file_path  =  models.CharField( max_length=100, default="", null=False)      #生成的文件路径
    # request_date      = models.DateTimeField(default=timezone.now())
    request_date      =  models.CharField( max_length= 50, default="", null=False)

    action_statue     =  models.CharField( max_length= 20, default=0, null=False)     #0,已经处理完毕, 1正在处理中, -1 错误

    username          =  models.CharField( max_length=200, default="", null=False)    #属于哪个用户的记录

    class Meta:
        db_table = "generate_report_tb"

    def __unicode__(self):
        return self.reportType




class AllStatements(models.Model):

    id           =  models.AutoField(primary_key=True, null=False)
    username          =  models.CharField( max_length=200, default="", null=False)    #属于哪个用户的记录

    settlement_period     = models.CharField( max_length=150, default="", null=False)
    beginning_balance     = models.CharField( max_length=100, default="", null=False)
    product_charges_total = models.CharField( max_length=100, default="", null=False)
    promo_retates_total   = models.CharField( max_length=100, default="", null=False)
    amazon_fees_total     = models.CharField( max_length=100, default="", null=False)
    other_total           = models.CharField( max_length=100, default="", null=False)
    deposit_total         = models.CharField( max_length=100, default="", null=False)
    actions               = models.CharField( max_length=10, default="0", null=False)

    filename              = models.CharField( max_length=200 ,default="", null=False)

    date_time             = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = "all_statements_tb"
    def __unicode__(self):
        return self.settlement_period


class TransactionView(models.Model):
    id          =   models.AutoField( primary_key=True, null=False)
    username          =  models.CharField( max_length=200, default="", null=False)    #属于哪个用户的记录


    filter_view  = models.CharField( max_length=200, default="", null=False)
    transaction_type = models.CharField( max_length=200, default="", null=False)
    order_id         = models.CharField( max_length=100, default="", null=False)
    product_details  = models.CharField( max_length=350, default="", null=False)
    total_product_charges = models.CharField( max_length=100, default="0.00", null=False)
    total_promotional_rebates = models.CharField( max_length=100, default="0.00", null=False)
    amazon_fees           = models.CharField( max_length=100, default="0.00", null=False)
    other                 = models.CharField( max_length=100, default="0.00", null=False)
    total                 = models.CharField( max_length=100, default="0.00", null=False)

    date_time             = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = "transaction_view_tb"

    def __unicode__(self):
        return self.transaction_type



class InventoryReports(models.Model):
    
    id            =   models.AutoField( primary_key=True,null=False)
    username          =  models.CharField( max_length=200, default="", null=False)    #属于哪个用户的记录

    report_type   =   models.CharField( max_length=100, default="", null=False)
    batch_id      =   models.CharField( max_length=100, default="", null=False)
    date_time_request     =   models.CharField( max_length=100, default="", null=False)
    date_time_completed   =   models.CharField( max_length=100, default="", null=False)
    report_status         =   models.CharField( max_length=100, default="", null=False)
    fileName              =   models.CharField( max_length=100, default="", null=False)

    class Meta:
        db_table = "inventory_reports_tb"
    def __unicode__(self):
        return  self.report_type


class InventoryReportsData(models.Model):
    """ Inventory Report的数据 """
    id            =  models.AutoField( primary_key=True, null=False)
    username      =  models.CharField( max_length=200, default="", null=False)

    filename      =  models.CharField( max_length=100, default="", null=False)    #锁属于的文件名

    seller_sku              = models.CharField( max_length=100, default="", null=False)    #
    fulfillment_channel_sku = models.CharField( max_length=100, default="", null=False)
    asin                    = models.CharField( max_length=50,  default="", null=False)    #
    condition_type          = models.CharField( max_length=100, default="", null=False)
    Warehouse_Condition_code= models.CharField( max_length=100, default="", null=False)
    Quantity_Available      = models.CharField( max_length=50,  default="", null=False)

    class Meta:
        db_table = "inventory_report_data"

    def __unicode__(self):
        return self.seller_sku












