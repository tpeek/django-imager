from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone


PRIVACY = [('Private', 'Private'),
           ('Shared', 'Shared'),
           ('Public', 'Public')]


@python_2_unicode_compatible
class Photo(models.Model):
    file = models.ImageField(upload_to='photo_files/%Y-%m-%d')
    owner = models.ForeignKey(User, null=False, related_name='photos')
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    date_uploaded = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)
    date_published = models.DateTimeField(default=timezone.now)
    privacy = models.CharField(max_length=7, choices=PRIVACY, default='Public')

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Album(models.Model):
    photos = models.ManyToManyField(Photo, related_name='photos')
    cover = models.ForeignKey(Photo, related_name='cover', blank=True, null=True)
    owner = models.ForeignKey(User, null=False, related_name='albums')
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    date_uploaded = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)
    date_published = models.DateTimeField(default=timezone.now)
    privacy = models.CharField(max_length=7, choices=PRIVACY, default='Public')

    def __str__(self):
        return self.title
