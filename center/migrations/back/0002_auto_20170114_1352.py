# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryReportsData',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(default=b'', max_length=200)),
                ('filename', models.CharField(default=b'', max_length=100)),
                ('sku', models.CharField(default=b'', max_length=100)),
                ('asin', models.CharField(default=b'', max_length=50)),
                ('price', models.CharField(default=b'', max_length=50)),
                ('quantity', models.CharField(default=b'', max_length=50)),
            ],
            options={
                'db_table': 'inventory_report_data',
            },
        ),
        migrations.AlterField(
            model_name='allstatements',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 5, 52, 38, 452338, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactionview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 5, 52, 38, 452988, tzinfo=utc)),
        ),
    ]
