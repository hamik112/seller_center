# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0007_auto_20161224_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryreports',
            name='fileName',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='allstatements',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 6, 2, 37, 0, 200959, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactionview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 6, 2, 37, 0, 201487, tzinfo=utc)),
        ),
    ]
