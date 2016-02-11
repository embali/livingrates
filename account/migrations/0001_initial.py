# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(blank=True, max_length=255, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='last name')),
                ('email', models.EmailField(unique=True, verbose_name='email address', max_length=254)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Use for successful email confirmation.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('middle_name', models.CharField(blank=True, max_length=255, verbose_name='middle name')),
                ('confirmation', models.CharField(blank=True, max_length=128, verbose_name='confirmation')),
                ('is_banned', models.BooleanField(default=False, verbose_name='banned', help_text='Designates whether this user should be treated as banned. Select this instead of deleting accounts.')),
                ('expiration', models.DateTimeField(default=django.utils.timezone.now, verbose_name='expiration')),
                ('new_email', models.EmailField(blank=True, max_length=254, verbose_name='new email address')),
                ('mailed', models.DateTimeField(default=django.utils.timezone.now, verbose_name='mailed')),
                ('groups', models.ManyToManyField(blank=True, related_name='user_set', verbose_name='groups', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_set', verbose_name='user permissions', to='auth.Permission', help_text='Specific permissions for this user.', related_query_name='user')),
            ],
            options={
                'verbose_name': 'account',
                'verbose_name_plural': 'accounts',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
