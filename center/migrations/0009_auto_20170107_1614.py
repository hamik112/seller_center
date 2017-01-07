# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0008_auto_20170106_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allstatements',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 7, 8, 14, 58, 331443, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactionview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 7, 8, 14, 58, 332062, tzinfo=utc)),
        ),
    ]
