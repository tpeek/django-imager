from __future__ import unicode_literals
from .models import ImagerProfile
from django.contrib.auth.models import User
from django.test import TestCase
import factory


class UserFactory(factory.Factory):
    class Meta:
        model = User
    email = factory.LazyAttribute(lambda x: '{}.example.com'.format(x.username))
    username = factory.Sequence(lambda n: 'user{}'.format(n))


class ProfileTestCase1(TestCase):
    def setUp(self):
        self.user = UserFactory.create(username='bob', email='b@b.com')
        self.user.set_password('secret')

    def test_profile_made_with_user(self):
        self.assertTrue(ImagerProfile.objects.count() == 0)
        self.user.save()
        self.assertTrue(ImagerProfile.objects.count() == 1)

    def test_is_active(self):
        self.assertTrue(self.user.is_active)
    # def test_profile_is_username(self):
    #     profile = ImagerProfile.objects.get(user=self.user)
    #     #self.assertEqual(str(profile), "bob")


# class ProfileTestCase2(TestCase):
#     def setUp(self):
#     self.user = UserFactory.build()


class ProfileTestCase3(TestCase):
    def setUp2(self):
        self.users = []
        user = UserFactory()
