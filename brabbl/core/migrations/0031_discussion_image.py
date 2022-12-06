# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_statement_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/discussion/', null=True, verbose_name='Image'),
        ),
    ]
