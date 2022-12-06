# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20151110_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='_replyto_email',
            field=models.EmailField(blank=True, help_text='Falls leer, wird die Moderatorenadresse genutzt.', max_length=254, verbose_name='ReplyTo email'),
        ),
    ]
