# Generated by Django 2.2.9 on 2020-11-25 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_alter_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_representative_name',
            field=models.CharField(blank=True, default='', max_length=191),
        ),
        migrations.AddField(
            model_name='customer',
            name='public_customer_name',
            field=models.CharField(blank=True, default='', max_length=191),
        ),
    ]