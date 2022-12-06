# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20160721_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='wording',
            name='button_new_contra',
            field=models.CharField(help_text='Write new argument', blank=True, max_length=64,
                                   verbose_name='Button Contra', default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='button_new_pro',
            field=models.CharField(help_text='Write new argument', blank=True, max_length=64, verbose_name='Button Pro',
                                   default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='button_short_new_contra',
            field=models.CharField(help_text='Write new argument', blank=True, max_length=64,
                                   verbose_name='Button Contra', default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='button_short_new_pro',
            field=models.CharField(help_text='Write new argument', blank=True, max_length=64, verbose_name='Button Pro',
                                   default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='header_contra',
            field=models.CharField(help_text='Contra-Argument', blank=True, max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='header_pro',
            field=models.CharField(help_text='Pro-Argument', blank=True, max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='list_header_contra',
            field=models.CharField(help_text='CONTRA', blank=True, max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='list_header_pro',
            field=models.CharField(help_text='PRO', blank=True, max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='rating_1',
            field=models.CharField(help_text='very poor', blank=True, max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='rating_2',
            field=models.CharField(help_text='poor', blank=True, max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='rating_3',
            field=models.CharField(help_text='ok', blank=True, max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='rating_4',
            field=models.CharField(help_text='good', blank=True, max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='rating_5',
            field=models.CharField(help_text='very good', blank=True, max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='reply_counter',
            field=models.CharField(help_text='Reply', blank=True, max_length=64, verbose_name='Name singular',
                                   default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='reply_counter_plural',
            field=models.CharField(help_text='Replies', blank=True, max_length=64, verbose_name='Plural name',
                                   default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='statement_header',
            field=models.CharField(help_text='Reply', blank=True, max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='statement_list_header',
            field=models.CharField(help_text='Answer', blank=True, max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='survey_add_answer_button_bottom',
            field=models.CharField(help_text='Write new statement', blank=True, max_length=64,
                                   verbose_name='Bottom button', default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='survey_add_answer_button_top',
            field=models.CharField(help_text='Write new statement', blank=True, max_length=64,
                                   verbose_name='Top button', default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='survey_statement',
            field=models.CharField(help_text='Statement', blank=True, max_length=64, verbose_name='Name singular',
                                   default=''),
        ),
        migrations.AddField(
            model_name='wording',
            name='survey_statements',
            field=models.CharField(help_text='Statements', blank=True, max_length=64, verbose_name='Plural name',
                                   default=''),
        ),
    ]
