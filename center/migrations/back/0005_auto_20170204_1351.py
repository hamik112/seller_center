# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0004_auto_20170118_0539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventoryreportsdata',
            old_name='price',
            new_name='Quantity_Available',
        ),
        migrations.RenameField(
            model_name='inventoryreportsdata',
            old_name='sku',
            new_name='Warehouse_Condition_code',
        ),
        migrations.RemoveField(
            model_name='inventoryreportsdata',
            name='quantity',
        ),
        migrations.AddField(
            model_name='inventoryreportsdata',
            name='condition_type',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='inventoryreportsdata',
            name='fulfillment_channel_sku',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='inventoryreportsdata',
            name='seller_sku',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='allstatements',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 4, 5, 51, 35, 835364, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactionview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 4, 5, 51, 35, 835896, tzinfo=utc)),
        ),
    ]
