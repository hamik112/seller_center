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
        migrations.AlterField(
            model_name='filenametostorename',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 5, 52, 38, 454903, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='filenametostorename',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 5, 52, 38, 454922, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='statementview',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 5, 52, 38, 455962, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 5, 52, 38, 455553, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storekeys',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 5, 52, 38, 455571, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='uploadfilerecorde',
            name='uploadtime',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 14, 5, 52, 38, 454404, tzinfo=utc)),
        ),
    ]
