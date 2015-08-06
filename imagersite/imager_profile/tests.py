from __future__ import unicode_literals
from .models import ImagerProfile
from django.contrib.auth.models import User
import factory
from django.test import Client, TestCase
from imager_images.models import Photo, Album
from faker import Factory as FakeFaker
from django.conf import settings
import os
from django.db import IntegrityError

fake = FakeFaker.create()


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


class PhotoFactory(factory.Factory):
    class Meta:
        model = Photo
    title = fake.sentence()
    description = fake.paragraph()


class ImagerProfileFactory(factory.Factory):
    class Meta:
        model = ImagerProfile


class AlbumFactory(factory.Factory):
    class Meta:
        model = Album
    title = fake.sentence()
    description = fake.paragraph()


class ProfileModelTestCase1(TestCase):
    def setUp(self):
        self.user = UserFactory.create(username='Penelope')
        self.user.set_password('secret')

    def test_profile_made_and_destroyed_with_user(self):
        self.assertTrue(ImagerProfile.objects.count() == 0)
        self.user.save()
        self.assertTrue(ImagerProfile.objects.count() == 1)

    def test_user_made_and_destroyed_with_profile(self):
        self.user.save()
        self.assertTrue(User.objects.count() == 1)
        profile = ImagerProfileFactory.create()
        with self.assertRaises(IntegrityError):
            profile.save()

    def test_profile_is_full_name(self):
        self.user.save()
        profile = ImagerProfile.objects.get(user=self.user)
        full_name = "{} {}".format(self.user.first_name, self.user.last_name)
        self.assertEqual(str(profile), full_name)


class ProfileTest(TestCase):
    """Tests for Profile view"""
    def setUp(self):
        """Make a User no photos"""
        self.client = Client()
        # Fake data
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        # Create user
        self.user = User.objects.create_user(username=self.username,
            password=self.password, email=self.email)
        self.login = self.client.post('/login/', {'username': self.username,
            'password': self.password}, follow=True)

    def test_count_no_photos(self):
        viewprof = self.client.get('/profile/')
        self.assertIn('>0</', viewprof.content)
        # Should do this check; a non logged in response could potentially
        # also display zero photos
        self.assertIn(self.username, viewprof.content)

    def test_count_photos_no_albums(self):
        viewprof = self.client.get('/profile/')
         # Add a couple photos to the user we created
        photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        photo1.save()
        photo2.save()
        response = self.client.get('/profile/')

        # Number of photos
        self.assertIn('>2</', response.content)
        # Number of albums
        self.assertIn('>0</', response.content)

    def test_count_photos_one_albums(self):
        viewprof = self.client.get('/profile/')

        # Add a couple photos to the user we created
        photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        photo1.save()
        photo2.save()
        album = AlbumFactory.create(owner=self.user, cover=photo1)
        album.save()
        album.photos = [photo1, photo2]
        response = self.client.get('/profile/')

        # Number of photos
        self.assertIn('>2</', response.content)
        # Number of albums
        self.assertIn('>1</', response.content)

    def test_check_links(self):
        response = self.client.get('/profile/')
        self.assertIn('href="/images/library/"', response.content)
        self.assertIn('/profile/edit/', response.content)

    def test_profile_after_user_login(self):
        self.assertEqual(self.login.wsgi_request.path, '/profile/')


class EditProfile(TestCase):
    def setUp(self):
        self.client = Client()
        # Fake data
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        # Create user
        self.user = User.objects.create_user(username=self.username,
            password=self.password, email=self.email)
        self.login = self.client.post('/login/', {'username': self.username,
            'password': self.password}, follow=True)

    def test_has_form(self):
        response = self.client.get('/profile/edit/')
        self.assertTrue(response.context['user_form'])
        self.assertTrue(response.context['profile_form'])
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_has_populated_data(self):
        response = self.client.get('/profile/edit/')
        self.assertIn(self.username, response.content)
        self.assertIn(self.email, response.content)

    def test_profile_post_edit_data(self):
        fields = dict(nickname=fake.name(), email=fake.email(),
            camera=fake.sentence(), address=fake.address(),
            website_url=fake.url(), photography_type='A')
        response = self.client.post('/profile/edit/', data=fields)
        self.assertEqual(response.status_code, 200)
