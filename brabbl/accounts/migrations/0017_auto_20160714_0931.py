# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20160502_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='language',
            field=models.CharField(max_length=2, choices=[('en', 'English'), ('de', 'Deutsch')], default='en'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='_replyto_email',
            field=models.EmailField(max_length=254, verbose_name='ReplyTo email', help_text='If left empty, the address of the moderator will be used.', blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='allowed_domains',
            field=models.TextField(help_text='One domain per line.'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(verbose_name='Creation date', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='deleted_at',
            field=models.DateTimeField(editable=False, verbose_name='Deletion date', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='modified_at',
            field=models.DateTimeField(verbose_name='Modified date', auto_now=True),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='key',
            field=models.CharField(max_length=64, choices=[('confirm_registration', 'Email asking for confirmation of account.'), ('welcome', 'Email asking for confirmation of account.'), ('daily_summary', 'Daily Summary')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='activated_at',
            field=models.DateTimeField(editable=False, verbose_name='Date of activation', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='deleted_at',
            field=models.DateTimeField(editable=False, verbose_name='Deletion date', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(verbose_name='Profile picture', null=True, upload_to='images/profiles/', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_sent',
            field=models.DateTimeField(verbose_name='Latest news mail delivery', auto_now_add=True, null=True),
        ),
    ]
