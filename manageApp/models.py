from django.db import models

from django.utils import timezone
# Create your models here.


class UploadFileRecorde(models.Model):
    id         =  models.AutoField(primary_key=True,null=False)
    filename   =  models.CharField( max_length=255, default="", null=False)
    file_path  =  models.CharField( max_length=500, default="", null=False)

    uploadtime =  models.DateTimeField( default= timezone.now())

    class Meta:
        db_table = "upload_file_recorde"

    def __unicode__(self):
        return self.filename



class StatementView(models.Model):
    id              =  models.AutoField( primary_key=True, null=False)
    date_time    =  models.CharField( max_length=50, default="", null=False)

    settlement_id   =  models.CharField( max_length=50, default="", null=False)
    type            =  models.CharField( max_length=50, default="", null=False)
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

    class Meta:
        db_table = "statement_view"

    def __unicode__(self):
        return self.store_name

