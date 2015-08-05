# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0013_photo_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='location',
            new_name='geom',
        ),
    ]
