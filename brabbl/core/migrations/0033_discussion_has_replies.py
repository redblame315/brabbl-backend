# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_argument_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='has_replies',
            field=models.BooleanField(default=True),
        ),
    ]
