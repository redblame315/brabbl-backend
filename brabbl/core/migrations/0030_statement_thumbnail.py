# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20161101_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
