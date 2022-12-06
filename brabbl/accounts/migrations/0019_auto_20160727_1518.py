# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import social.apps.django_app.default.fields
import social.storage.django_orm


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20160720_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSocialAuth',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('provider', models.CharField(max_length=32)),
                ('uid', models.CharField(max_length=255)),
                ('extra_data', social.apps.django_app.default.fields.JSONField(default='{}')),
            ],
            options={
                'db_table': 'accounts_usersocialauth',
            },
            bases=(models.Model, social.storage.django_orm.DjangoUserMixin),
        ),
        migrations.AddField(
            model_name='customer',
            name='auth_back_link',
            field=models.URLField(default='', blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='usersocialauth',
            name='customer',
            field=models.ForeignKey(related_name='customer_social_auth', to='accounts.Customer', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='usersocialauth',
            name='user',
            field=models.ForeignKey(related_name='custom_social_auth', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=94, unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        ),
        migrations.AlterUniqueTogether(
            name='usersocialauth',
            unique_together=set([('provider', 'uid', 'customer')]),
        ),
    ]
