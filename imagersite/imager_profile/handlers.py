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


@receiver(post_save, sender=ImagerProfile)
def create_user(sender, **kwargs):
    """An ImagerProfile should always have a User"""
    instance = kwargs.get('instance')
    if not instance or kwargs.get('raw', False):
        return
    try:
        instance.user
    except User.DoesNotExist:
        instance.user = User()
        instance.user.save()


@receiver(post_delete, sender=ImagerProfile)
def rm_user_profile(sender, **kwargs):
    """If an ImagerProfile is deleted, delete it's User too"""
    instance = kwargs.get('instance')
    if not instance:
        return
    try:
        instance.user.delete()
    except:
        pass


@receiver(post_delete, sender=User)
def rm_user(sender, **kwargs):
    """If a User is deleted, delete it's ImagerProfile too"""
    instance = kwargs.get('instance')
    if not instance:
        return
    try:
        instance.profile.delete()
    except:
        pass
