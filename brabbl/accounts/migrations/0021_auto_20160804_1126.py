# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social.apps.django_app.default.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_custom_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='default_wording',
            field=models.IntegerField(default=0),
        ),
    ]
