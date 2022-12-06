# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_discussion_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='argument',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Active'), (2, 'Hidden')], default=1),
        ),
    ]
