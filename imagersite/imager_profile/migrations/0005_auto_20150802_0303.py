# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0004_auto_20150802_0153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagerprofile',
            name='name',
        ),
        migrations.AddField(
            model_name='imagerprofile',
            name='nickname',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='address',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='camera',
            field=models.CharField(help_text=b'What is the make and model of your camera?', max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='photography_type',
            field=models.CharField(blank=True, max_length=64, null=True, help_text=b'What is your photography type?', choices=[(b'H', b'Hobbist'), (b'A', b'Abstract'), (b'B', b'Black and White'), (b'P', b'Panorama'), (b'J', b'Journalism')]),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='website_url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
