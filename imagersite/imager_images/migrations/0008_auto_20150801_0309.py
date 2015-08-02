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
            field=models.ForeignKey(related_name='cover', blank=True, to='imager_images.Photo'),
        ),
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='privacy',
            field=models.CharField(default=b'Public', max_length=7, choices=[(b'Private', b'Private'), (b'Shared', b'Shared'), (b'Public', b'Public')]),
        ),
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='privacy',
            field=models.CharField(default=b'Public', max_length=7, choices=[(b'Private', b'Private'), (b'Shared', b'Shared'), (b'Public', b'Public')]),
        ),
    ]
