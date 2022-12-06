# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social.apps.django_app.default.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20160808_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('language', models.CharField(max_length=2, choices=[('en', 'English'), ('de', 'Deutsch')], default='en')),
                ('email_sign', models.TextField(help_text='Allowed parameters: {{domain}}')),
            ],
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='key',
            field=models.CharField(max_length=64, choices=[('confirm_registration', 'Email asking for confirmation of account.'), ('daily_summary', 'Daily Summary.'), ('forgot_password', 'Forgot Password.'), ('argument_flagging', 'Argument flagging.')]),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='subject',
            field=models.CharField(max_length=1024, help_text='Allowed parameters: {{domain}}, and {{username}}, {{firstname}}, {{lastname}} if type is not Argument flagging.'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='text',
            field=models.TextField(help_text='Allowed parameters: {{domain}}, and {{username}}, {{firstname}}, {{lastname}} if type is not Argument flagging.'),
        ),
        migrations.AddField(
            model_name='customer',
            name='email_group',
            field=models.ForeignKey(default=None, blank=True, null=True, to='accounts.EmailGroup', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='email_group',
            field=models.ForeignKey(to='accounts.EmailGroup', default='', on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]
