# Generated by Django 2.2.9 on 2021-01-21 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0043_auto_20210121_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email_sign',
            field=models.TextField(blank=True, default='', help_text='Allowed parameters: {{domain}}', null=True),
        ),
    ]
