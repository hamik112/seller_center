# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0003_generatereport_report_file_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatereport',
            name='username',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
