# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20160811_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='language',
            field=models.CharField(max_length=2, default='en', choices=[('en', 'English'), ('de', 'Deutsch'), ('es', 'Spanish'), ('fr', 'French'), ('it', 'Italian'), ('el', 'Greek'), ('uk', 'Ukrainian'), ('ru', 'Russian')]),
        ),
        migrations.AlterField(
            model_name='notificationwordingmessage',
            name='notification_wording',
            field=models.ForeignKey(related_name='notification_wording_messages', to='core.NotificationWording', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='wording',
            name='language',
            field=models.CharField(max_length=2, default='en', choices=[('en', 'English'), ('de', 'Deutsch'), ('es', 'Spanish'), ('fr', 'French'), ('it', 'Italian'), ('el', 'Greek'), ('uk', 'Ukrainian'), ('ru', 'Russian')]),
        ),
    ]
