from .models import ImagerProfile
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=User)
def create_user_profile(sender, **kwargs):
    """A User should always have an ImagerProfile"""
    instance = kwargs.get('instance')
    if not instance or kwargs.get('raw', False):
        return
    try:
        instance.profile
    except ImagerProfile.DoesNotExist:
        instance.profile = ImagerProfile()
        instance.profile.save()


@receiver(post_delete, sender=ImagerProfile)
def rm_user_profile(sender, **kwargs):
    """If an ImagerProfile is deleted, delete it's User too"""
    instance = kwargs.get('instance')
    if not instance:
        return
    instance.user.delete()
