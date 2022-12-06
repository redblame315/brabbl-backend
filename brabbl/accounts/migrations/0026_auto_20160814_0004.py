# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import social.apps.django_app.default.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20160811_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='language',
            field=models.CharField(max_length=2, default='en', choices=[('en', 'English'), ('de', 'Deutsch'), ('es', 'Spanish'), ('fr', 'French'), ('it', 'Italian'), ('el', 'Greek'), ('uk', 'Ukrainian'), ('ru', 'Russian')]),
        ),
        migrations.AlterField(
            model_name='emailgroup',
            name='language',
            field=models.CharField(max_length=2, default='en', choices=[('en', 'English'), ('de', 'Deutsch'), ('es', 'Spanish'), ('fr', 'French'), ('it', 'Italian'), ('el', 'Greek'), ('uk', 'Ukrainian'), ('ru', 'Russian')]),
        ),
    ]
