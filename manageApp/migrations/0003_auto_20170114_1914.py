# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0002_auto_20170114_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryUploadRecorde',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('filename', models.CharField(default=b'', unique=True, max_length=255)),
                ('file_path', models.CharField(default=b'', max_length=500)),
                ('file_statue', models.CharField(default=b'0', max_length=10)),
                ('error_msg', models.CharField(default=b'', max_length=300)),
                ('uploadtime', models.DateTimeField(default=datetime.datetime(2017, 1, 14, 11, 14, 25, 965884, tzinfo=utc))),
            ],
            options={
                'db_table': 'inventory_upload_recorde',
            },
        ),
        migrations.AlterField(
            model_name='filenametostorename',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 11, 14, 25, 967011, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='filenametostorename',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 11, 14, 25, 967069, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='statementview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 11, 14, 25, 968887, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 11, 14, 25, 968442, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 11, 14, 25, 968462, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='uploadfilerecorde',
            name='uploadtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 11, 14, 25, 965427, tzinfo=utc)),
        ),
    ]
