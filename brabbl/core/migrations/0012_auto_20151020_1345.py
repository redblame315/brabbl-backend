# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20151015_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barometervote',
            name='value',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '3')]),
        ),
        migrations.AlterField(
            model_name='statement',
            name='barometer_value',
            field=models.DecimalField(default=0, decimal_places=1, max_digits=2, editable=False),
        ),
    ]
