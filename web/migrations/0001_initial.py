# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('address', models.TextField(db_index=True, unique=True, verbose_name='address')),
                ('latitude', models.FloatField(null=True, db_index=True, verbose_name='latitude')),
                ('longitude', models.FloatField(null=True, db_index=True, verbose_name='longitude')),
            ],
            options={
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('value', models.FloatField(null=True, verbose_name='value')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('image', models.ImageField(upload_to='', max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('apartment', models.CharField(max_length=32, verbose_name='apartment', blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('text', models.TextField(verbose_name='text', blank=True)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('address', models.ForeignKey(to='web.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Variety',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('category', models.ForeignKey(to='web.Category')),
            ],
            options={
                'verbose_name_plural': 'varieties',
            },
        ),
        migrations.AddField(
            model_name='photo',
            name='rate',
            field=models.ForeignKey(to='web.Rate'),
        ),
        migrations.AddField(
            model_name='grade',
            name='rate',
            field=models.ForeignKey(to='web.Rate'),
        ),
        migrations.AddField(
            model_name='grade',
            name='variety',
            field=models.ForeignKey(to='web.Variety'),
        ),
    ]
