# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import brabbl.accounts.managers


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20151013_1400'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', brabbl.accounts.managers.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='activated_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Löschungsdatem', editable=False),
        ),
    ]
