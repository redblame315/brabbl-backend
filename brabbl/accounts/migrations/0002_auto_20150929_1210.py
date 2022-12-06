# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='customer',
            field=models.ForeignKey(to='accounts.Customer', null=True, blank=True, on_delete=models.CASCADE),
        ),
    ]
