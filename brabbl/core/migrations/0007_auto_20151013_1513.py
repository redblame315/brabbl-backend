# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151013_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discussion',
            old_name='has_multiple_statements',
            new_name='multiple_statements_allowed',
        ),
    ]
