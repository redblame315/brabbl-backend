# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151001_1443'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discussion',
            old_name='multiple_statements',
            new_name='has_multiple_statements',
        ),
    ]
