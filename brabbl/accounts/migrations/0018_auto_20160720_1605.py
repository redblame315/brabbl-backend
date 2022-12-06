# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20160714_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='default_back_link',
            field=models.URLField(max_length=128, default='', blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='default_back_title',
            field=models.CharField(max_length=64, default='', blank=True),
        ),
    ]
