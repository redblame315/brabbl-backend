# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150929_1210'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_tag_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(verbose_name='Erstellungsdatum', auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Löschungsdatem', editable=False)),
                ('external_id', models.CharField(max_length=256, unique=True, db_index=True)),
                ('source_url', models.URLField()),
                ('image', models.URLField(blank=True)),
                ('main_statement', models.CharField(max_length=1024)),
                ('multiple_statements', models.BooleanField(default=False)),
                ('barometer_wording', models.ForeignKey(null=True, to='core.Wording', blank=True, on_delete=models.CASCADE)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('customer', models.ForeignKey(to='accounts.Customer', on_delete=models.CASCADE)),
                ('tags', models.ManyToManyField(to='core.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
