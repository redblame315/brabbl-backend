# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social.apps.django_app.default.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20160814_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerUserInfoSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=64)),
                ('show_in_profile', models.BooleanField(default=False)),
                ('show_in_welcome', models.BooleanField(default=False)),
                ('is_required', models.BooleanField(default=False)),
                ('property_model', models.ForeignKey(related_name='model_properties', to='accounts.Customer', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='bundesland',
            field=models.CharField(choices=[('AT-1', 'Burgenland'), ('AT-2', 'Kärnten'), ('AT-3', 'Niederösterreich'), ('AT-4', 'Oberösterreich'), ('AT-5', 'Salzburg'), ('AT-6', 'Steiermark'), ('AT-7', 'Tirol'), ('AT-8', 'Vorarlberg'), ('AT-9', 'Wien'), ('', 'Anders Land')], default='', blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(null=True, default='', blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(null=True, default='', blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Whatever'), (1, 'Male'), (2, 'Female')], default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.CharField(null=True, default='', blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='user',
            name='postcode',
            field=models.CharField(null=True, default='', blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='user',
            name='year_of_birth',
            field=models.PositiveSmallIntegerField(default=None, blank=True, null=True),
        ),
    ]
