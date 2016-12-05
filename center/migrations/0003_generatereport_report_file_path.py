# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0002_auto_20161205_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatereport',
            name='report_file_path',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
