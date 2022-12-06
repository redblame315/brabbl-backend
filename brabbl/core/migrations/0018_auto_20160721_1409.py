# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20160714_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='discussion',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
