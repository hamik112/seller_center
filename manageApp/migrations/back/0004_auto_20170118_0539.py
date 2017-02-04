# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0003_auto_20170114_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filenametostorename',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 21, 39, 19, 633903, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='filenametostorename',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 21, 39, 19, 633943, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='inventoryuploadrecorde',
            name='uploadtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 21, 39, 19, 632725, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='statementview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 21, 39, 19, 636338, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 21, 39, 19, 635248, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 21, 39, 19, 635285, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='uploadfilerecorde',
            name='uploadtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 21, 39, 19, 631846, tzinfo=utc)),
        ),
    ]
