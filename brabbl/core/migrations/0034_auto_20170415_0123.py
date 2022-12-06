# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_discussion_has_replies'),
    ]

    operations = [
        migrations.AddField(
            model_name='argument',
            name='original_rating_count_of_hidden_argument',
            field=models.PositiveIntegerField(editable=False, default=0),
        ),
        migrations.AddField(
            model_name='argument',
            name='original_rating_of_hidden_argument',
            field=models.DecimalField(max_digits=2, editable=False, default=0, decimal_places=1),
        ),
    ]
