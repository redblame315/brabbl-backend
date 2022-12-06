# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20160304_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='newsmail_schedule',
            field=models.IntegerField(blank=True, choices=[(1, 'daily'), (7, 'weekly')], default=1, null=True),
        ),
    ]
