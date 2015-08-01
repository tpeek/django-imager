# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('camera', models.CharField(help_text=b'What is the make and mofel of your camera?', max_length=128)),
                ('address', models.TextField()),
                ('wesite_url', models.URLField()),
                ('photography_type', models.CharField(help_text=b'What is your photography type?', max_length=1, choices=[(b'H', b'Hobbist'), (b'A', b'Abstract'), (b'B', b'Black and White'), (b'P', b'Panorama'), (b'J', b'Journalism')])),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
