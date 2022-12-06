# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20151104_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('de', 'Deutsch')], default='en', max_length=2),
        ),
        migrations.AddField(
            model_name='wording',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('de', 'Deutsch')], default='en', max_length=2),
        ),
        migrations.AlterField(
            model_name='argument',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='argument',
            name='deleted_at',
            field=models.DateTimeField(verbose_name='Deletion date', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='argument',
            name='last_related_activity',
            field=models.DateTimeField(verbose_name='Last activity', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='argument',
            name='modified_at',
            field=models.DateTimeField(verbose_name='Modified date', auto_now=True),
        ),
        migrations.AlterField(
            model_name='barometervote',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='barometervote',
            name='deleted_at',
            field=models.DateTimeField(verbose_name='Deletion date', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='barometervote',
            name='modified_at',
            field=models.DateTimeField(verbose_name='Modified date', auto_now=True),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='deleted_at',
            field=models.DateTimeField(verbose_name='Deletion date', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='last_related_activity',
            field=models.DateTimeField(verbose_name='Last activity', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='modified_at',
            field=models.DateTimeField(verbose_name='Modified date', auto_now=True),
        ),
        migrations.AlterField(
            model_name='flag',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='flag',
            name='deleted_at',
            field=models.DateTimeField(verbose_name='Deletion date', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='flag',
            name='modified_at',
            field=models.DateTimeField(verbose_name='Modified date', auto_now=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='deleted_at',
            field=models.DateTimeField(verbose_name='Deletion date', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='modified_at',
            field=models.DateTimeField(verbose_name='Modified date', auto_now=True),
        ),
        migrations.AlterField(
            model_name='statement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='deleted_at',
            field=models.DateTimeField(verbose_name='Deletion date', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='statement',
            name='last_related_activity',
            field=models.DateTimeField(verbose_name='Last activity', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='statement',
            name='modified_at',
            field=models.DateTimeField(verbose_name='Modified date', auto_now=True),
        ),
        migrations.AlterField(
            model_name='wording',
            name='customer',
            field=models.ForeignKey(help_text='Leave blank to make available to all customers.', blank=True, null=True, to='accounts.Customer', on_delete=models.CASCADE),
        ),
    ]
