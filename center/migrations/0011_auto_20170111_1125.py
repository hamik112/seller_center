# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0010_auto_20170111_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allstatements',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 11, 3, 25, 4, 662171, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactionview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 11, 3, 25, 4, 662762, tzinfo=utc)),
        ),
    ]
