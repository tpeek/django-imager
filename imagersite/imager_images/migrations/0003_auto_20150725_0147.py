# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('imager_images', '0002_delete_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('date_uploaded', models.DateTimeField(default=datetime.datetime(2015, 7, 25, 1, 47, 7, 903792))),
                ('date_modified', models.DateTimeField(default=datetime.datetime(2015, 7, 25, 1, 47, 7, 903812))),
                ('date_published', models.DateTimeField(default=datetime.datetime(2015, 7, 25, 1, 47, 7, 903829))),
                ('privacy', models.CharField(max_length=64, choices=[(b'PR', b'private'), (b'SH', b'shared'), (b'PU', b'public')])),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(upload_to=b'photo_files/%Y-%m-%d')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('date_uploaded', models.DateTimeField(default=datetime.datetime(2015, 7, 25, 1, 47, 7, 902944))),
                ('date_modified', models.DateTimeField(default=datetime.datetime(2015, 7, 25, 1, 47, 7, 902970))),
                ('date_published', models.DateTimeField(default=datetime.datetime(2015, 7, 25, 1, 47, 7, 902986))),
                ('privacy', models.CharField(max_length=64, choices=[(b'PR', b'private'), (b'SH', b'shared'), (b'PU', b'public')])),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(related_name='cover', to='imager_images.Photo'),
        ),
        migrations.AddField(
            model_name='album',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(related_name='photos', to='imager_images.Photo'),
        ),
    ]
