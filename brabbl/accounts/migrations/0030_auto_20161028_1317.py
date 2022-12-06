# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social.apps.django_app.default.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_auto_20161004_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='theme',
            field=models.CharField(max_length=24, default='brabbl', choices=[('bjv', 'Bjv'), ('brabbl', 'Brabbl'), ('eyp', 'Eyp'), ('vorwaerts', 'Vorwaerts')]),
        ),
    ]
