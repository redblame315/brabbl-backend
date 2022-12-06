# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20160502_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='newsmail_schedule',
            field=models.IntegerField(choices=[(None, 'never'), (1, 'daily'), (7, 'weekly')], blank=True, null=True),
        ),
    ]
