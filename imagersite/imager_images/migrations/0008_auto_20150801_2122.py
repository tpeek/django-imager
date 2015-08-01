# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0007_auto_20150729_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(related_name='cover', to='imager_images.Photo', null=True),
        ),
    ]
