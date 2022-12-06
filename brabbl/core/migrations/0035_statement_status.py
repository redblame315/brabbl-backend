# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20170415_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, 'Active'), (2, 'Hidden')]),
        ),
    ]
