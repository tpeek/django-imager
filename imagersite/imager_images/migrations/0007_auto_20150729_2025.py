# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0006_auto_20150729_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='owner',
            field=models.ForeignKey(related_name='albums', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='photo',
            name='owner',
            field=models.ForeignKey(related_name='photos', to=settings.AUTH_USER_MODEL),
        ),
    ]
