# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20151014_1314'),
    ]

    operations = [
        migrations.RenameField(
            model_name='argument',
            old_name='user',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='argument',
            old_name='is_positive',
            new_name='is_pro',
        ),
        migrations.AlterField(
            model_name='argument',
            name='rating_count',
            field=models.PositiveIntegerField(editable=False, default=0),
        ),
        migrations.AlterField(
            model_name='argument',
            name='reply_to',
            field=models.ForeignKey(null=True, blank=True, to='core.Argument', related_name='replies', on_delete=models.CASCADE),
        ),
    ]
