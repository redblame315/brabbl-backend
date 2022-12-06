# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def update_username_during_migration(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    for user in User.objects.all():
        embed_token = ""
        if user.customer_id:
            embed_token = "+" + user.customer.embed_token
        user.username = user.username + embed_token
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20160727_1518'),
    ]

    operations = [
        migrations.RunPython(update_username_during_migration),
    ]
