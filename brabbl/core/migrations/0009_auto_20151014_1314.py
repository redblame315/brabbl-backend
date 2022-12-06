# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_discussion_user_can_add_replies'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 10, 14, 11, 14, 13, 560147, tzinfo=utc), verbose_name='Erstellungsdatum'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='statement',
            name='deleted_at',
            field=models.DateTimeField(editable=False, blank=True, verbose_name='Löschungsdatem', null=True),
        ),
        migrations.AddField(
            model_name='statement',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 10, 14, 11, 14, 22, 672009, tzinfo=utc), verbose_name='Änderungsdatum'),
            preserve_default=False,
        ),
    ]
