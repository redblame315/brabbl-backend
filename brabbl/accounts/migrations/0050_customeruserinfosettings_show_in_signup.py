# Generated by Django 2.2.24 on 2021-08-27 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0049_auto_20210825_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeruserinfosettings',
            name='show_in_signup',
            field=models.BooleanField(default=False),
        ),
    ]
