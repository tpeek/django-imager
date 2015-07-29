# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0005_auto_20150728_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='privacy',
            field=models.CharField(max_length=64, choices=[(b'Private', b'Private'), (b'Shared', b'Shared'), (b'Public', b'Public')]),
        ),
        migrations.AlterField(
            model_name='photo',
            name='privacy',
            field=models.CharField(max_length=64, choices=[(b'Private', b'Private'), (b'Shared', b'Shared'), (b'Public', b'Public')]),
        ),
    ]
