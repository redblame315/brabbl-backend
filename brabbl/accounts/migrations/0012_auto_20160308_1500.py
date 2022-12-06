# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20160304_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='receives_email_notifications',
            field=models.BooleanField(verbose_name='Newsmail-Abo', default=False),
        ),
    ]
