# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151013_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='user_can_add_replies',
            field=models.BooleanField(default=False),
        ),
    ]
