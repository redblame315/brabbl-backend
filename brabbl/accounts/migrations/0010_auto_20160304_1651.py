# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20151117_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_sent',
            field=models.DateTimeField(verbose_name='Letzer Newsmail-Versand', auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='newsmail_schedule',
            field=models.IntegerField(choices=[(1, 'daily'), (7, 'weekly')], blank=True, default=1),
        ),
    ]
