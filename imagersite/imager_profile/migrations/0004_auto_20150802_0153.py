# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0003_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagerprofile',
            old_name='wesite_url',
            new_name='website_url',
        ),
    ]
