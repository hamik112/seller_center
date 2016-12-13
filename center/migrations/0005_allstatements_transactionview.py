# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0004_generatereport_username'),
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
                ('date_time', models.DateTimeField(default=datetime.datetime(2016, 12, 13, 2, 26, 13, 564775, tzinfo=utc))),
            ],
            options={
                'db_table': 'all_statements_tb',
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
                ('date_time', models.DateTimeField(default=datetime.datetime(2016, 12, 13, 2, 26, 13, 565380, tzinfo=utc))),
            ],
            options={
                'db_table': 'transaction_view_tb',
            },
        ),
    ]
