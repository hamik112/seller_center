# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0002_auto_20170214_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filenametostorename',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 21, 168770, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='filenametostorename',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 21, 168789, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='inventoryuploadrecorde',
            name='uploadtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 21, 168254, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='statementview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 21, 169811, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 21, 169399, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 21, 169417, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='uploadfilerecorde',
            name='uploadtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 21, 167698, tzinfo=utc)),
        ),
    ]
