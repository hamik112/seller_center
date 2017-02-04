# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0004_auto_20170118_0539'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfilerecorde',
            name='serial_number',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='filenametostorename',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 4, 5, 51, 35, 838976, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='filenametostorename',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 4, 5, 51, 35, 838996, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='inventoryuploadrecorde',
            name='uploadtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 4, 5, 51, 35, 838269, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='statementview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 4, 5, 51, 35, 840039, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 4, 5, 51, 35, 839621, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 4, 5, 51, 35, 839639, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='uploadfilerecorde',
            name='uploadtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 4, 5, 51, 35, 837680, tzinfo=utc)),
        ),
    ]
