from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


class ActiveProfileManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProfileManager,
                     self).get_queryset().filter(user__is_active=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    PHOTOGRAPHY_CHOICES = [('H', 'Hobbist'),
                           ('A', 'Abstract'),
                           ('B', 'Black and White'),
                           ('P', 'Panorama'),
                           ('J', 'Journalism'), ]
    nickname = models.CharField(max_length=128, null=True, blank=True)
    user = models.OneToOneField(User, related_name="profile")
    camera = models.CharField(max_length=128,
                        help_text="What is the make and model of your camera?",
                        null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    photography_type = models.CharField(
        max_length=64, help_text="What is your photography type?",
        choices=PHOTOGRAPHY_CHOICES, null=True, blank=True)
    objects = models.Manager()
    active = ActiveProfileManager()

    def __str__(self):
        return self.nickname or self.user.get_full_name() or self.user.username

    def get_photo_type(self):
        types = {'H': 'Hobbist',
                 'A': 'Abstract',
                 'B': 'Black and White',
                 'P': 'Panorama',
                 'J': 'Journalism'}
        return types[self.photography_type]

    @property
    def is_active(self):
        return self.user.is_active
