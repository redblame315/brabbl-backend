# Generated by Django 2.2.9 on 2021-06-04 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0047_auto_20210604_1620'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='auto_update_interval_for_customer',
            new_name='auto_update_interval',
        ),
    ]