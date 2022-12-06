# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customer_flag_count_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='replyto_email',
            new_name='_replyto_email',
        ),
    ]
