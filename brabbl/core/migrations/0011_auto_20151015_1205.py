# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20151014_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='argument',
            name='rating_value',
            field=models.DecimalField(decimal_places=1, default=3, max_digits=2, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='argument',
            name='statement',
            field=models.ForeignKey(related_name='arguments', to='core.Statement', on_delete=models.CASCADE),
        ),
    ]
