# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20160804_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='auth_back_link',
        ),
    ]
