# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0003_auto_20150725_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='album',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='album',
            name='date_uploaded',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_uploaded',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
