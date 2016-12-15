# encoding:utf-8
from django.db import models

from django.utils import timezone
# Create your models here.






class UploadFileRecorde(models.Model):
    """ 记录上传的文件 """
    id         =  models.AutoField(primary_key=True,null=False)
    filename   =  models.CharField( max_length=255, default="", unique=True, null=False)
    file_path  =  models.CharField( max_length=500, default="", null=False)
    file_statue = models.CharField( max_length= 10, default="0", null=False)  #状态，是否正在更新
    error_msg   = models.CharField( max_length= 300, default="", null=False)

    uploadtime =  models.DateTimeField( default= timezone.now())

    class Meta:
        db_table = "upload_file_recorde"
    def __unicode__(self):
        return self.filename



class FilenameToStorename(models.Model):
    """ 文件名与店铺的对应 """
    id              =  models.AutoField( primary_key=True, null=False)
    filename        =  models.CharField( max_length= 300, null=False)
    serial_number   =  models.CharField( max_length=50, default="", unique=True,null=False)
    storename       =  models.CharField( max_length= 100,default="", null=False)
    email           =  models.CharField( max_length= 50, default="",unique=True, null=False)      #email即是用户名不能重复
    password        =  models.CharField( max_length= 100, default="starmerx", null=False)

    create_time     =  models.DateTimeField( default=timezone.now())
    update_time     =  models.DateTimeField( default=timezone.now())

    class Meta:
        db_table = "filename_to_storename"

    def __unicode__(self):
        return self.filename

    def get_serial_number(self):
        return u'%s' % (self.serial_number)



class StatementView(models.Model):
    """ date range reports 报表"""
    id              =  models.AutoField( primary_key=True, null=False)
    # date_time    =  models.CharField( max_length=50, default="", null=False)
    # unique_id       = models.CharField( max_length=200, default="", unique=True, null=False)   #时间加order_id为唯一标识
    date_time       = models.DateTimeField( default=timezone.now(), null=False)

    filename        =  models.CharField( max_length=100, default="", null=False)

    settlement_id   =  models.CharField( max_length=50, default="", null=False)
    type            =  models.CharField( max_length=200, default="", null=False)
    order_id        =  models.CharField( max_length=100, default="", null=False)
    sku             =  models.CharField( max_length=50, default="", null=False)
    description     =  models.CharField( max_length=200, default="", null=False)
    quantity        =  models.CharField( max_length=50 , default="", null=False)
    marketplace     =  models.CharField( max_length=50, default="", null=False)
    fulfillment     =  models.CharField( max_length=50, default="", null=False)
    order_city      =  models.CharField( max_length=50, default="", null=False)
    order_state     =  models.CharField( max_length=50, default="", null=False)
    order_postal    =  models.CharField( max_length=50, default="", null=False)

    product_sales   =  models.CharField( max_length= 50, default="0", null=False)
    shipping_credits = models.CharField( max_length=50 , default="0", null=False)
    gift_wrap_credits= models.CharField( max_length=50, default="0", null=False)
    promotional_rebates = models.CharField( max_length=50, default="0", null=False)
    sales_tax_collected = models.CharField( max_length=50, default="0", null=False)
    selling_fees     = models.CharField( max_length=50, default="0", null=False)
    fba_fees         = models.CharField( max_length=50, default="0", null=False)
    other_transaction_fees = models.CharField( max_length=50, default='0', null=False)
    other            = models.CharField( max_length=50, default="0", null=False)
    total            = models.CharField( max_length=50, default="0", null=False)
    store_name       = models.CharField( max_length=50, default="", null=False)

    # 序号，代表了店铺名，来源于文件名的序号
    serial_number    = models.CharField( max_length=50, default="", null=False)
    area             = models.CharField( max_length=100, default="", null=False)
    class Meta:
        db_table = "statement_view"

    def __unicode__(self):
        return self.store_name

