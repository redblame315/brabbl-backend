# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20160815_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscussionList',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('deleted_at', models.DateTimeField(verbose_name='Deletion date', null=True, editable=False, blank=True)),
                ('url', models.URLField(unique=True, db_index=True)),
                ('name', models.CharField(max_length=160)),
                ('search_by', models.PositiveSmallIntegerField(choices=[(1, 'Show all'), (1, 'Search by any tag'), (2, 'Search by all tags')])),
                ('hide_tag_filter_for_users', models.BooleanField(default=False)),
                ('tags', models.ManyToManyField(blank=True, to='core.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
