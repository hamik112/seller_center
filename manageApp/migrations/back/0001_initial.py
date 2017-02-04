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
            name='FilenameToStorename',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('filename', models.CharField(max_length=300)),
                ('serial_number', models.CharField(default=b'', unique=True, max_length=50)),
                ('gateway_name', models.CharField(default=b'', max_length=50)),
                ('storename', models.CharField(default=b'', max_length=100)),
                ('manager', models.CharField(default=b'', max_length=100)),
                ('email', models.CharField(default=b'', unique=True, max_length=100)),
                ('new_card', models.CharField(default=b'', max_length=100)),
                ('kdt_card', models.CharField(default=b'', max_length=100)),
                ('old_card', models.CharField(default=b'', max_length=100)),
                ('seller_id', models.CharField(default=b'', max_length=50)),
                ('amazon_key_id', models.CharField(default=b'', max_length=50)),
                ('amazon_key', models.CharField(default=b'', max_length=50)),
                ('password', models.CharField(default=b'starmerx', max_length=100)),
                ('really_store', models.CharField(default=b'0', max_length=10)),
                ('payment_time', models.CharField(default=b'', max_length=30)),
                ('create_time', models.DateTimeField(default=datetime.datetime(2017, 1, 12, 1, 39, 9, 669654, tzinfo=utc))),
                ('update_time', models.DateTimeField(default=datetime.datetime(2017, 1, 12, 1, 39, 9, 669672, tzinfo=utc))),
            ],
            options={
                'db_table': 'filename_to_storename',
            },
        ),
        migrations.CreateModel(
            name='StatementView',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date_time', models.DateTimeField(default=datetime.datetime(2017, 1, 12, 1, 39, 9, 670739, tzinfo=utc))),
                ('filename', models.CharField(default=b'', max_length=100)),
                ('settlement_id', models.CharField(default=b'', max_length=50)),
                ('type', models.CharField(default=b'', max_length=200)),
                ('order_id', models.CharField(default=b'', max_length=100)),
                ('sku', models.CharField(default=b'', max_length=50)),
                ('description', models.CharField(default=b'', max_length=200)),
                ('quantity', models.CharField(default=b'', max_length=50)),
                ('marketplace', models.CharField(default=b'', max_length=50)),
                ('fulfillment', models.CharField(default=b'', max_length=50)),
                ('order_city', models.CharField(default=b'', max_length=50)),
                ('order_state', models.CharField(default=b'', max_length=50)),
                ('order_postal', models.CharField(default=b'', max_length=50)),
                ('product_sales', models.CharField(default=b'0', max_length=50)),
                ('shipping_credits', models.CharField(default=b'0', max_length=50)),
                ('gift_wrap_credits', models.CharField(default=b'0', max_length=50)),
                ('promotional_rebates', models.CharField(default=b'0', max_length=50)),
                ('sales_tax_collected', models.CharField(default=b'0', max_length=50)),
                ('selling_fees', models.CharField(default=b'0', max_length=50)),
                ('fba_fees', models.CharField(default=b'0', max_length=50)),
                ('other_transaction_fees', models.CharField(default=b'0', max_length=50)),
                ('other', models.CharField(default=b'0', max_length=50)),
                ('total', models.CharField(default=b'0', max_length=50)),
                ('store_name', models.CharField(default=b'', max_length=50)),
                ('serial_number', models.CharField(default=b'', max_length=50)),
                ('area', models.CharField(default=b'', max_length=100)),
            ],
            options={
                'db_table': 'statement_view',
            },
        ),
        migrations.CreateModel(
            name='StoreKeys',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.CharField(default=b'', unique=True, max_length=100)),
                ('storename', models.CharField(default=b'', max_length=100)),
                ('access_key', models.CharField(default=b'', max_length=50)),
                ('secret_key', models.CharField(default=b'', max_length=100)),
                ('account_id', models.CharField(default=b'', max_length=100)),
                ('mkplaceid', models.CharField(default=b'', max_length=50)),
                ('mws_authtoken', models.CharField(default=b'', unique=True, max_length=150)),
                ('create_time', models.DateTimeField(default=datetime.datetime(2017, 1, 12, 1, 39, 9, 670335, tzinfo=utc))),
                ('update_time', models.DateTimeField(default=datetime.datetime(2017, 1, 12, 1, 39, 9, 670353, tzinfo=utc))),
            ],
            options={
                'db_table': 'store_key',
            },
        ),
        migrations.CreateModel(
            name='UploadFileRecorde',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('filename', models.CharField(default=b'', unique=True, max_length=255)),
                ('file_path', models.CharField(default=b'', max_length=500)),
                ('file_statue', models.CharField(default=b'0', max_length=10)),
                ('error_msg', models.CharField(default=b'', max_length=300)),
                ('uploadtime', models.DateTimeField(default=datetime.datetime(2017, 1, 12, 1, 39, 9, 669154, tzinfo=utc))),
            ],
            options={
                'db_table': 'upload_file_recorde',
            },
        ),
    ]
