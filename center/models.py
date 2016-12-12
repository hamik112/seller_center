# encoding:utf-8


from django.db import models

from django.utils import  timezone
# Create your models here.


class GenerateReport(models.Model):
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

    action_statue     =  models.CharField( max_length= 20, default=0, null=False)

    username          =  models.CharField( max_length=200, default="", null=False)    #属于哪个用户的记录

    class Meta:
        db_table = "generate_report_tb"

    def __unicode__(self):
        return self.reportType


