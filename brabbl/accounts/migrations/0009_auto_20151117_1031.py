# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20151111_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='allowed_domains',
            field=models.TextField(help_text='Eine domain pro Zeile.'),
        ),
    ]
