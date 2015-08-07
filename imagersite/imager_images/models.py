from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone


PRIVACY = [('Private', 'Private'),
           ('Shared', 'Shared'),
           ('Public', 'Public')]


class Face(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()


@python_2_unicode_compatible
class Photo(models.Model):
    faces = models.ManyToManyField(Face, related_name='photos', blank=True, null=True)
    file = models.ImageField(upload_to='photo_files/%Y-%m-%d')
    owner = models.ForeignKey(User, null=False, related_name='photos')
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(max_length=7, choices=PRIVACY, default='Public')
    geom = geomodels.PointField(null=True, blank=True)

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
