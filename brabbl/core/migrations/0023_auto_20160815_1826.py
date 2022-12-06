# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20160814_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationwordingmessage',
            name='notification_wording',
        ),
        migrations.AddField(
            model_name='notificationwordingmessage',
            name='property_model',
            field=models.ForeignKey(related_name='model_properties', to='core.NotificationWording', default='', on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]
