# Generated by Django 2.2.24 on 2022-12-28 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0055_auto_20221215_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.PositiveIntegerField(default=0)),
                ('argument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Argument')),
                ('discussion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Discussion')),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Statement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'discussion', 'statement', 'argument')},
            },
        ),
    ]