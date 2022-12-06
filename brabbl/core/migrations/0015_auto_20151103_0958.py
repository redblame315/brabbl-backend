# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20151029_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barometervote',
            name='value',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='wordingvalue',
            name='value',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
    ]
