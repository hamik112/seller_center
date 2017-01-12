# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllStatements',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(default=b'', max_length=200)),
                ('settlement_period', models.CharField(default=b'', max_length=150)),
                ('beginning_balance', models.CharField(default=b'', max_length=100)),
                ('product_charges_total', models.CharField(default=b'', max_length=100)),
                ('promo_retates_total', models.CharField(default=b'', max_length=100)),
                ('amazon_fees_total', models.CharField(default=b'', max_length=100)),
                ('other_total', models.CharField(default=b'', max_length=100)),
                ('deposit_total', models.CharField(default=b'', max_length=100)),
                ('actions', models.CharField(default=b'0', max_length=10)),
                ('filename', models.CharField(default=b'', max_length=200)),
                ('date_time', models.DateTimeField(default=datetime.datetime(2017, 1, 12, 1, 39, 4, 507958, tzinfo=utc))),
            ],
            options={
                'db_table': 'all_statements_tb',
            },
        ),
        migrations.CreateModel(
            name='GenerateReport',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('is_custom', models.CharField(default=b'', max_length=30)),
                ('reportType', models.CharField(default=b'', max_length=30)),
                ('year', models.CharField(default=b'', max_length=200)),
                ('timeRangeType', models.CharField(default=b'', max_length=100)),
                ('month', models.CharField(default=b'', max_length=100)),
                ('timeRange', models.CharField(default=b'', max_length=50)),
                ('report_file_path', models.CharField(default=b'', max_length=100)),
                ('request_date', models.CharField(default=b'', max_length=50)),
                ('action_statue', models.CharField(default=0, max_length=20)),
                ('username', models.CharField(default=b'', max_length=200)),
            ],
            options={
                'db_table': 'generate_report_tb',
            },
        ),
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
                ('fileName', models.CharField(default=b'', max_length=100)),
            ],
            options={
                'db_table': 'inventory_reports_tb',
            },
        ),
        migrations.CreateModel(
            name='TransactionView',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(default=b'', max_length=200)),
                ('filter_view', models.CharField(default=b'', max_length=200)),
                ('transaction_type', models.CharField(default=b'', max_length=200)),
                ('order_id', models.CharField(default=b'', max_length=100)),
                ('product_details', models.CharField(default=b'', max_length=350)),
                ('total_product_charges', models.CharField(default=b'0.00', max_length=100)),
                ('total_promotional_rebates', models.CharField(default=b'0.00', max_length=100)),
                ('amazon_fees', models.CharField(default=b'0.00', max_length=100)),
                ('other', models.CharField(default=b'0.00', max_length=100)),
                ('total', models.CharField(default=b'0.00', max_length=100)),
                ('date_time', models.DateTimeField(default=datetime.datetime(2017, 1, 12, 1, 39, 4, 508545, tzinfo=utc))),
            ],
            options={
                'db_table': 'transaction_view_tb',
            },
        ),
    ]
