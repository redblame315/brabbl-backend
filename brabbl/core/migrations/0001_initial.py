# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Wording',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=1024)),
                ('customer', models.ForeignKey(blank=True, null=True, help_text='Leer lassen, um für alle Kunden verfügbar zu machen.', to='accounts.Customer', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='WordingValue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=1024)),
                ('value', models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '3')])),
                ('wording', models.ForeignKey(related_name='words', to='core.Wording', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='wordingvalue',
            unique_together=set([('wording', 'value')]),
        ),
    ]
