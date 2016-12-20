# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0005_allstatements_transactionview'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryReports',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(default=b'', max_length=200)),
                ('report_type', models.CharField(default=b'', max_length=100)),
                ('batch_id', models.CharField(default=b'', max_length=100)),
                ('date_time_request', models.CharField(default=b'', max_length=100)),
                ('date_time_completed', models.CharField(default=b'', max_length=100)),
                ('report_status', models.CharField(default=b'', max_length=100)),
            ],
            options={
                'db_table': 'inventory_reports_tb',
            },
        ),
        migrations.AddField(
            model_name='allstatements',
            name='actions',
            field=models.CharField(default=b'0', max_length=10),
        ),
        migrations.AddField(
            model_name='allstatements',
            name='filename',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='allstatements',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 20, 10, 15, 21, 620176, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactionview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 20, 10, 15, 21, 620791, tzinfo=utc)),
        ),
    ]
