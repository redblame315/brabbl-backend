# Generated by Django 2.2.9 on 2020-12-01 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20201201_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='wording',
            name='description',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='discussionlist',
            name='url',
            field=models.URLField(db_index=True, null=True, unique=True),
        ),
    ]
