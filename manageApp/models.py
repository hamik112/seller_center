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

