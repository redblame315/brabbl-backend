# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_discussion'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarometerVote',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(verbose_name='Erstellungsdatum', auto_now_add=True)),
                ('modified_at', models.DateTimeField(verbose_name='Änderungsdatum', auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, verbose_name='Löschungsdatem', null=True)),
                ('value', models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '3')])),
            ],
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('statement', models.CharField(blank=True, max_length=1024)),
                ('barometer_count', models.PositiveIntegerField(editable=False, default=0)),
                ('barometer_value', models.DecimalField(decimal_places=1, max_digits=2, editable=False, null=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='discussion',
            name='has_arguments',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='discussion',
            name='has_barometer',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='discussion',
            name='statement',
            field=models.CharField(max_length=255, default='Test Statement'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='discussion',
            unique_together=set([('external_id', 'customer')]),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('customer', 'name')]),
        ),
        migrations.AddField(
            model_name='statement',
            name='discussion',
            field=models.ForeignKey(to='core.Discussion', related_name='statements', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='barometervote',
            name='statement',
            field=models.ForeignKey(to='core.Statement', related_name='barometer_votes', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='barometervote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.RemoveField(
            model_name='discussion',
            name='main_statement',
        ),
        migrations.AlterUniqueTogether(
            name='barometervote',
            unique_together=set([('statement', 'user')]),
        ),
    ]
