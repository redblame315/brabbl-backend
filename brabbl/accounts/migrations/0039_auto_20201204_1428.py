# Generated by Django 2.2.9 on 2020-12-04 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_customer_available_wordings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='available_wordings',
            field=models.ManyToManyField(to='core.Wording'),
        ),
    ]