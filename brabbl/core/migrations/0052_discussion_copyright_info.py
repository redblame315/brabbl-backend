# Generated by Django 2.2.24 on 2021-08-24 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_auto_20210820_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='copyright_info',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
