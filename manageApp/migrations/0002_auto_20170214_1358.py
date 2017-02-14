# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storekeys',
            old_name='storename',
            new_name='gateway_name',
        ),
        migrations.AlterField(
            model_name='filenametostorename',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 0, 95120, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='filenametostorename',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 0, 95137, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='inventoryuploadrecorde',
            name='uploadtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 0, 94613, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='statementview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 0, 96155, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 0, 95717, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 0, 95734, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='uploadfilerecorde',
            name='uploadtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 14, 5, 58, 0, 94098, tzinfo=utc)),
        ),
    ]
