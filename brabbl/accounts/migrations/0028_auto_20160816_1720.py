# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import social.apps.django_app.default.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20160815_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.CharField(max_length=128, default='', blank=True, null=True),
        ),
    ]
