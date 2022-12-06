# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20160831_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarkdownWordingMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('key', models.CharField(db_index=True, max_length=64)),
                ('value', models.TextField(blank=True, default='')),
                ('property_model', models.ForeignKey(to='core.NotificationWording', related_name='model_markdown_properties', on_delete=models.CASCADE)),
            ],
        ),
    ]
