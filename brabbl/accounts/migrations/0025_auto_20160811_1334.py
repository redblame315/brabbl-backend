# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social.apps.django_app.default.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20160810_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='displayed_username',
            field=models.IntegerField(choices=[(1, 'Username'), (2, 'First name + Last name')], default=1),
        ),
        migrations.AddField(
            model_name='customer',
            name='notification_wording',
            field=models.IntegerField(default=0),
        )
    ]
