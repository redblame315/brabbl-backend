# Generated by Django 2.2.24 on 2022-12-16 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20221215_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
