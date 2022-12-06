# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20151110_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activated_at',
            field=models.DateTimeField(editable=False, verbose_name='Aktivierungsdatum', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='deleted_at',
            field=models.DateTimeField(editable=False, verbose_name='Löschungsdatum', blank=True, null=True),
        ),
    ]
