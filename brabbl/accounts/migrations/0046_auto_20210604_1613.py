# Generated by Django 2.2.9 on 2021-06-04 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0045_customer_are_private_discussions_allowed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auto_update_interval_for_admins',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='auto_update_interval_for_customer',
            field=models.IntegerField(default=0),
        ),
    ]
