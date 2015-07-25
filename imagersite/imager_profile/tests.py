from __future__ import unicode_literals
from .models import ImagerProfile
from django.contrib.auth.models import User
from django.test import TestCase
import factory


class UserFactory(factory.Factory):
    class Meta:
        model = User
    email = factory.LazyAttribute(
        lambda x: '{}@{}.com'.format(x.username, x.username[::-1]).lower())
    username = factory.Sequence(lambda n: 'user{}'.format(n))


class ProfileTestCase1(TestCase):
    def setUp(self):
        self.user = UserFactory.create(username='Penelope')
        self.user.set_password('secret')

    def test_profile_made_and_destroyed_with_user(self):
        self.assertTrue(ImagerProfile.objects.count() == 0)
        self.user.save()
        self.assertTrue(ImagerProfile.objects.count() == 1)
        self.user.delete()
        self.assertTrue(ImagerProfile.objects.count() == 0)

    def test_profile_is_username(self):
        self.user.save()
        profile = ImagerProfile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'Penelope')
