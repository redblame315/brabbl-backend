# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_discussionlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussionlist',
            name='search_by',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Show all'), (2, 'Search by any tag'), (3, 'Search by all tags')]),
        ),
    ]
