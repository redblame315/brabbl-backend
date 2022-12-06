# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20160823_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='barometer_wording',
            field=models.ForeignKey(null=True, verbose_name='Wording', blank=True, to='core.Wording', on_delete=models.CASCADE),
        ),
    ]
