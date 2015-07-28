# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='camera',
            field=models.CharField(help_text=b'What is the make and model of your camera?', max_length=128),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='photography_type',
            field=models.CharField(help_text=b'What is your photography type?', max_length=64, choices=[(b'H', b'Hobbist'), (b'A', b'Abstract'), (b'B', b'Black and White'), (b'P', b'Panorama'), (b'J', b'Journalism')]),
        ),
    ]
