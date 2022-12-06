# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social.apps.django_app.default.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20161124_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='default_has_replies',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='theme',
            field=models.CharField(default='brabbl', choices=[('bjv', 'Bjv'), ('brabbl', 'Brabbl'), ('eyp', 'Eyp'), ('vorwaerts', 'Vorwaerts'), ('jugendinfo', 'Jugendinfo')], max_length=24),
        ),
    ]
