# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social.apps.django_app.default.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('accounts', '0030_auto_20161028_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user_groups',
            field=models.ManyToManyField(to='auth.Group', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='bundesland',
            field=models.CharField(max_length=5, choices=[('AT-1', 'Burgenland'), ('AT-2', 'Kärnten'), ('AT-3', 'Niederösterreich'), ('AT-4', 'Oberösterreich'), ('AT-5', 'Salzburg'), ('AT-6', 'Steiermark'), ('AT-7', 'Tirol'), ('AT-8', 'Vorarlberg'), ('AT-9', 'Wien'), ('-', 'Anders Land')], default='', blank=True),
        ),
    ]
