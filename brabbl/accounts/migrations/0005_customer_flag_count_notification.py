# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20151028_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='flag_count_notification',
            field=models.IntegerField(default=10),
        ),
    ]
