# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatereport',
            name='request_date',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
