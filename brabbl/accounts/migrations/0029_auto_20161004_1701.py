# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_auto_20160816_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_confirmed',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='key',
            field=models.CharField(choices=[('confirm_registration', 'Email asking for confirmation of account.'), ('daily_summary', 'Daily Summary.'), ('forgot_password', 'Forgot Password.'), ('argument_flagging', 'Argument flagging.'), ('non_active_user_warning', 'Non active user warning.')], max_length=64),
        ),
    ]
