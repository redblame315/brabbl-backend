# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('created_at', models.DateTimeField(verbose_name='Erstellungsdatum', auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum')),
                ('deleted_at', models.DateTimeField(editable=False, null=True, verbose_name='Löschungsdatem', blank=True)),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], max_length=30, verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('receives_email_notifications', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(verbose_name='Erstellungsdatum', auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum')),
                ('deleted_at', models.DateTimeField(editable=False, null=True, verbose_name='Löschungsdatem', blank=True)),
                ('name', models.CharField(max_length=1024)),
                ('embed_token', models.CharField(unique=True, max_length=64)),
                ('allowed_domains', models.TextField(blank=True)),
                ('moderator_email', models.EmailField(max_length=254)),
                ('replyto_email', models.EmailField(max_length=254, help_text='Falls leer, wird die Moderatorenadresse genutzt.', blank=True)),
                ('after_confirmation_url', models.URLField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('key', models.CharField(max_length=64, choices=[('confirm_registration', 'Frage nach Bestätigung'), ('welcome', 'Willkommensmail nach erfolgreicher Bestätigung'), ('daily_summary', 'Tägliche Zusammenfassung')])),
                ('subject', models.CharField(max_length=1024)),
                ('text', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='customer',
            field=models.ForeignKey(to='accounts.Customer', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(verbose_name='groups', to='auth.Group', related_query_name='user', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', related_query_name='user', related_name='user_set', help_text='Specific permissions for this user.', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('customer', 'username'), ('customer', 'email')]),
        ),
    ]
