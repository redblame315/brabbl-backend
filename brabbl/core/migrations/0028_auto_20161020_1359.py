# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_markdownwordingmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='image',
            field=models.ImageField(null=True, upload_to='images/statements/', verbose_name='Image', blank=True),
        ),
        migrations.AddField(
            model_name='statement',
            name='video',
            field=embed_video.fields.EmbedVideoField(null=True, verbose_name='Video', blank=True),
        ),
    ]
