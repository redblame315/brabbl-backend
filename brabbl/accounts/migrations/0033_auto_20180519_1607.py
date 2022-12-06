# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import social.apps.django_app.default.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_auto_20170316_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPolicy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=600)),
                ('text', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True)),
                ('version_number', models.DecimalField(unique=True, default=1.0, max_digits=6, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Datenschutz-Richtlinie',
                'verbose_name_plural': 'Datenschutz-Richtlinien',
            },
        ),
        migrations.CreateModel(
            name='DataPolicyAgreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP-Adresse', blank=True, null=True)),
                ('date_accepted', models.DateTimeField(verbose_name='Zustimmung am')),
                ('data_policy', models.ForeignKey(to='accounts.DataPolicy', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Datenschutz-Zustimmung',
                'verbose_name_plural': 'Datenschutz-Zustimmungen',
                'get_latest_by': 'date_accepted',
            },
        ),
        migrations.AddField(
            model_name='datapolicyagreement',
            name='user',
            field=models.ForeignKey(related_name='datapolicyagreements', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='customer',
            name='data_policy_version',
            field=models.ForeignKey(blank=True, null=True, to='accounts.DataPolicy', on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='datapolicyagreement',
            unique_together=set([('user', 'data_policy')]),
        ),
    ]
