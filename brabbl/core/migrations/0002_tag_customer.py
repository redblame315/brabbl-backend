# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150929_1210'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='customer',
            field=models.ForeignKey(default=1, to='accounts.Customer', on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]
