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
            name='GenerateReport',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('is_custom', models.CharField(default=b'', max_length=30)),
                ('reportType', models.CharField(default=b'', max_length=30)),
                ('year', models.CharField(default=b'', max_length=200)),
                ('timeRangeType', models.CharField(default=b'', max_length=100)),
                ('month', models.CharField(default=b'', max_length=100)),
                ('timeRange', models.CharField(default=b'', max_length=50)),
                ('request_date', models.DateTimeField(default=datetime.datetime(2016, 12, 2, 10, 6, 21, 392734, tzinfo=utc))),
                ('action_statue', models.CharField(default=0, max_length=20)),
            ],
            options={
                'db_table': 'generate_report_tb',
            },
        ),
    ]
