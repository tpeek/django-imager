from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


PRIVACY = [('PR', 'private'),
           ('SH', 'shared'),
           ('PU', 'public')]


@python_2_unicode_compatible
class Photo(models.Model):
    pic = models.ImageField(upload_to='photo_files/%Y-%m-%d')
    owner = models.ForeignKey(User, null=False)
    title = models.CharField(max_length=128)
    description = models.TextField()
    date_uploaded = models.DateTimeField('date uploaded')
    date_modified = models.DateTimeField('date modified')
    date_published = models.DateTimeField('date published')
    privacy = models.ChariField(max_length=64, choices=PRIVACY)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Album(models.Model):
    photos = models.ManyToManyField(Photo)
    cover = models.ForeignKey(Photo)
    owner = models.ForeignKey(User, null=False)
    title = models.CharField(max_length=128)
    description = models.TextField()
    date_uploaded = models.DateTimeField('date uploaded')
    date_modified = models.DateTimeField('date modified')
    date_published = models.DateTimeField('date published')
    privacy = models.ChariField(max_length=64, choices=PRIVACY)

    def __str__(self):
        return self.title
