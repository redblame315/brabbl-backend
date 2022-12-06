# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20151020_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='argument',
            name='last_related_activity',
            field=models.DateTimeField(null=True, verbose_name='Letzte Aktivität', editable=False),
        ),
        migrations.AddField(
            model_name='discussion',
            name='last_related_activity',
            field=models.DateTimeField(null=True, verbose_name='Letzte Aktivität', editable=False),
        ),
        migrations.AddField(
            model_name='statement',
            name='last_related_activity',
            field=models.DateTimeField(null=True, verbose_name='Letzte Aktivität', editable=False),
        ),
    ]
