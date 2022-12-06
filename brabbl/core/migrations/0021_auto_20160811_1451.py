# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20160808_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationWording',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=64, help_text='First create a model to see all messages')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationWordingMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=64)),
                ('value', models.TextField(default='', blank=True)),
                ('notification_wording', models.ForeignKey(to='core.NotificationWording', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterField(
            model_name='wording',
            name='name',
            field=models.CharField(unique=True, max_length=1024),
        ),
    ]
