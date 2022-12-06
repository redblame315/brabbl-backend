# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20151103_0958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discussion',
            old_name='image',
            new_name='image_url',
        ),
    ]
