from __future__ import unicode_literals
from .models import ImagerProfile
from django.contrib.auth.models import User
from django.test import TestCase
import factory
from faker import Faker

fake = Faker()


class UserFactory(factory.Factory):
    class Meta:
        model = User
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = factory.LazyAttribute(lambda a: '{}.{}@example.com'.format(
                                  a.first_name, a.last_name).lower())
    username = factory.LazyAttribute(lambda a: '{}{}{}{}'.format(
                                     a.last_name[:1], a.first_name[1:],
                                     a.first_name[:1], a.last_name[1:]).lower())


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

    def test_profile_is_full_name(self):
        self.user.save()
        profile = ImagerProfile.objects.get(user=self.user)
        full_name = "{} {}".format(self.user.first_name, self.user.last_name)
        self.assertEqual(str(profile), full_name)
