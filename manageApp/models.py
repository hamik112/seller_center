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
    product_sales   =  models.CharField( max_length= 20, default="0", null=False)
    shipping_credits = models.CharField( max_length=20 , default="0", null=False)
    gift_wrap_credits= models.CharField( max_length=20, default="0", null=False)
    promotional_rebates = models.CharField( max_length=20, default="0", null=False)
    sales_tax_collected = models.CharField( max_length=20, default="0", null=False)
    selling_fees     = models.CharField( max_length=20, default="0", null=False)
    fba_fees         = models.CharField( max_length=20, default="0", null=False)
    other_transaction_fees = models.CharField( max_length=20, default='0', null=False)
    other            = models.CharField( max_length=20, default="0", null=False)
    total            = models.CharField( max_length=20, default="0", null=False)
    store_name       = models.CharField( max_length=30, default="", null=False)

    class Meta:
        db_table = "statement_view"

    def __unicode__(self):
        return self.store_name

