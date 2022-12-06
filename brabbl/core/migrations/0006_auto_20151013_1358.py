# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_auto_20151001_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='Argument',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungsdatum')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum')),
                ('deleted_at', models.DateTimeField(editable=False, null=True, verbose_name='Löschungsdatem', blank=True)),
                ('is_positive', models.BooleanField()),
                ('title', models.CharField(max_length=1024)),
                ('text', models.TextField()),
                ('original_title', models.CharField(max_length=1024)),
                ('original_text', models.TextField()),
                ('rating_value', models.DecimalField(editable=False, null=True, decimal_places=1, max_digits=2)),
                ('rating_count', models.PositiveIntegerField(default=0)),
                ('reply_to', models.ForeignKey(null=True, to='core.Argument', blank=True, on_delete=models.CASCADE)),
                ('statement', models.ForeignKey(to='core.Statement', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungsdatum')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum')),
                ('deleted_at', models.DateTimeField(editable=False, null=True, verbose_name='Löschungsdatem', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungsdatum')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum')),
                ('deleted_at', models.DateTimeField(editable=False, null=True, verbose_name='Löschungsdatem', blank=True)),
                ('value', models.IntegerField()),
                ('argument', models.ForeignKey(related_name='ratings', to='core.Argument', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterField(
            model_name='barometervote',
            name='value',
            field=models.ForeignKey(to='core.WordingValue', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='external_id',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='tags',
            field=models.ManyToManyField(to='core.Tag', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('argument', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='flag',
            unique_together=set([('content_type', 'object_id', 'user')]),
        ),
    ]
