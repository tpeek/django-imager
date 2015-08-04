# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0012_auto_20150802_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
        ),
    ]
