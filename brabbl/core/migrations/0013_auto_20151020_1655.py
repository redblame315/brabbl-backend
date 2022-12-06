# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20151020_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='argument',
            name='rating_value',
            field=models.DecimalField(editable=False, decimal_places=1, default=3, max_digits=2),
        ),
        migrations.AlterField(
            model_name='rating',
            name='value',
            field=models.DecimalField(editable=False, decimal_places=1, max_digits=2),
        ),
    ]
