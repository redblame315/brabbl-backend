# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def reset_newsmail_schedule(apps, migration_schema):
    User = apps.get_model('accounts', 'user')
    for user in User.objects.all():
        if not user.receives_email_notifications:
            user.newsmail_schedule = None
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='newsmail_schedule',
            field=models.IntegerField(blank=True, choices=[(1, 'daily'), (7, 'weekly')], null=True),
        ),
        migrations.RunPython(reset_newsmail_schedule, lambda a, m: None),
        migrations.RemoveField(
            model_name='user',
            name='receives_email_notifications',
        ),
    ]
