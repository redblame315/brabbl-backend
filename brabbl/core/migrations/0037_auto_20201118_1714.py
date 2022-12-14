# Generated by Django 2.2.9 on 2020-11-18 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_alter_description_discussion'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociatedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.FileField(upload_to='private/', verbose_name='File')),
                ('discussion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='associated_files', to='core.Discussion')),
            ],
        ),
    ]