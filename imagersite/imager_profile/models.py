from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


class ActiveProfileManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProfileManager,
                     self).get_queryset().filter(user_is_active=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    PHOTOGRAPHY_CHOICES = [('H', 'Hobbist'),
                           ('A', 'Abstract'),
                           ('B', 'Black and White'),
                           ('P', 'Panorama'),
                           ('J', 'Journalism'), ]
    name = models.CharField(max_length=128)
    user = models.OneToOneField(User, related_name="profile")
    camera = models.CharField(
        max_length=128, help_text="What is the make and model of your camera?")
    address = models.TextField()
    website_url = models.URLField()
    photography_type = models.CharField(
        max_length=64, help_text="What is your photography type?",
        choices=PHOTOGRAPHY_CHOICES)
    objects = models.Manager()
    active = ActiveProfileManager()

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def is_active(self):
        return self.user.is_active
