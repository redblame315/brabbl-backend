# Generated by Django 2.2.9 on 2021-01-21 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0042_auto_20201204_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailgroup',
            name='email_sign',
        ),
        migrations.AddField(
            model_name='customer',
            name='email_sign',
            field=models.TextField(blank=True, default=None, help_text='Allowed parameters: {{domain}}', null=True),
        ),
    ]
